from flask import Blueprint, render_template, request, redirect, url_for

from . import db, models

bp = Blueprint("pages", __name__)


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
    all_cruises = db.session.execute(db.select(models.Cruise)).scalars().all()
    return render_template("info_request_create.html", cruises=all_cruises, message=request.args.get("message"))


@bp.post("/info_request/")
def create_info_request():
    name = request.form["name"]
    db_info_request = models.InfoRequest(name=name, email=request.form["email"], notes=request.form["notes"], cruise_id=request.form["cruise_id"])
    db.session.add(db_info_request)
    db.session.commit()
    success_message = f"Thank you, {name}! We will email you when we have more information!"
    return redirect(url_for('pages.info_request', message=success_message))
