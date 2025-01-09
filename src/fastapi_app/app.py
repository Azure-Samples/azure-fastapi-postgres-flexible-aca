import os
import pathlib
from typing import Annotated

from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .models import Cruise, Destination, InfoRequest, engine

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()

app = FastAPI()
parent_path = pathlib.Path(__file__).parent.parent
app.mount("/mount", StaticFiles(directory=parent_path / "static"), name="static")
templates = Jinja2Templates(directory=parent_path / "templates")
templates.env.globals["prod"] = os.environ.get("RUNNING_IN_PRODUCTION", False)
# Use relative path for url_for, so that it works behind a proxy like Codespaces
templates.env.globals["url_for"] = app.url_path_for


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/destinations", response_class=HTMLResponse)
def destinations(request: Request):
    with Session(engine) as session:
        all_destinations = session.exec(select(Destination)).all()
    return templates.TemplateResponse("destinations.html", {"request": request, "destinations": all_destinations})


@app.get("/destination/{pk}", response_class=HTMLResponse)
def destination_detail(request: Request, pk: int):
    with Session(engine) as session:
        destination = session.exec(select(Destination).where(Destination.id == pk)).first()
        return templates.TemplateResponse(
            "destination_detail.html", {"request": request, "destination": destination, "cruises": destination.cruises}
        )


@app.get("/cruise/{pk}")
def cruise_detail(request: Request, pk: int):
    with Session(engine) as session:
        cruise = session.exec(select(Cruise).where(Cruise.id == pk)).first()
        return templates.TemplateResponse(
            "cruise_detail.html", {"request": request, "cruise": cruise, "destinations": cruise.destinations}
        )


@app.get("/info_request/", response_class=HTMLResponse)
def info_request(request: Request):
    with Session(engine) as session:
        all_cruises = session.exec(select(Cruise)).all()
        return templates.TemplateResponse("info_request_create.html", {"request": request, "cruises": all_cruises})


@app.post("/info_request/", response_model=InfoRequest)
def create_info_request(request: Request, info_request: Annotated[InfoRequest, Form()]):
    with Session(engine) as session:
        session.add(info_request)
        session.commit()
        session.refresh(info_request)
        all_cruises = session.exec(select(Cruise)).all()
        return templates.TemplateResponse(
            "info_request_create.html",
            {
                "request": request,
                "cruises": all_cruises,
                "message": "Information request submitted.",
            },
        )
