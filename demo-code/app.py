from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import models
from sqlmodel import Session, select

app = FastAPI()
app.mount('/mount', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/destinations", response_class=HTMLResponse)
def destinations(request: Request):
    with Session(models.engine) as session:
        all_destinations = session.exec(select(models.Destination)).all()
    return templates.TemplateResponse("destinations.html", {"request": request, "destinations": all_destinations})


@app.get("/destination/{pk}", response_class=HTMLResponse)
def destination_detail(request: Request, pk: int):
    with Session(models.engine) as session:
        destination = session.exec(select(models.Destination).where(models.Destination.id==pk)).first()
        return templates.TemplateResponse("destination_detail.html", {"request": request, "destination": destination})

@app.get("/cruise/{pk}")
def cruise_detail(request: Request, pk: int):
    with Session(models.engine) as session:
        cruise = session.exec(select(models.Cruise).where(models.Cruise.id==pk)).first()
        return templates.TemplateResponse("cruise_detail.html", {"request": request, "cruise": cruise})


@app.get("/info_request/", response_class=HTMLResponse)
def info_request(request: Request):
    return templates.TemplateResponse("info_request_create.html", {"request": request})


@app.post("/info_request/", response_model=models.InfoRequest)
def create_info_request(info_request: models.InfoRequest):
    with Session(engine) as session:
        db_info_request = models.InfoRequest.from_orm(info_request)
        session.add(db_info_request)
        session.commit()
        session.refresh(db_info_request)
        return db_info_request