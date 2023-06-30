from flask import Blueprint, render_template, request

from . import db, models

bp = Blueprint("cruises", __name__)


@bp.get("/")
def index():
    return render_template("index.html")

@bp.get("/about")
def about():
    return render_template("about.html")

@bp.get("/destinations")
def destinations():
    all_destinations = db.session.execute(db.select(models.Destination)).scalars().all()
    return render_template("destinations.html", destinations=all_destinations)

@bp.get("/destination/<int:pk>")
def destination_detail(pk: int):
    destination = db.get_or_404(models.Destination, pk)
    return render_template("destination_detail.html", destination=destination)


@bp.get("/cruise/<int:pk>")
def cruise_detail(pk: int):
    cruise = db.get_or_404(models.Cruise, pk)
    return render_template("cruise_detail.html", cruise=cruise)


@bp.get("/info_request/")
def info_request():
    return render_template("info_request_create.html")


@bp.post("/info_request/")
def create_info_request():
    # make info request from form data
    db_info_request = models.InfoRequest(name=request.form["name"], email=request.form["email"], notes=request.form["notes"], cruise_id=request.form["cruise_id"])
    # save info request to database
    db.session.add(db_info_request)
    db.session.commit()
    return db_info_request
