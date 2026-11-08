import os

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Room, Service, Ticket, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "$H@AUL@"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

MEETING_LINK = "https://meet.google.com/abc-defg-hij"  # Provided by the teacher


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@app.template_global()
def ticket_label(t):
    """Label shown to people, e.g. PD08. Built from the service code and ticket id."""
    return f"{t.service.code}{t.id:02d}"


def all_services():
    """Services the join form offers: only the ones that are switched on."""
    return db.session.scalars(
        db.select(Service).where(Service.active).order_by(Service.id)
    ).all()


def current_room():
    """ClassQ has one default room for now (created by the seed command)."""
    return db.session.scalar(db.select(Room).order_by(Room.id))


# ---------------------------------------------------------------------------
# Part 7: Create (joining the queue) - uses the database
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    topic = form.get("topic", "").strip()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None
    room = current_room()

    errors = {}
    if not name:
        errors["name"] = "Enter your name or group name."
    elif len(name) > 60:
        errors["name"] = "Keep the name under 60 characters."
    if not topic:
        errors["topic"] = "Enter your topic or what you need help with."
    elif len(topic) > 150:
        errors["topic"] = "Keep the topic under 150 characters."
    if service is None or not service.active:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors=errors), 400

    if room is None:
        flash("The queue is not open yet. Ask your teacher.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 503

    ticket = Ticket(room=room, service=service, group_name=name, topic=topic)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if "ux_tickets_active_group_name" in str(e.orig):
            # The database stopped a double tap, or a second group with the same name.
            flash("That group is already in the queue.", "danger")
            return render_template("join.html", services=all_services(), form=form,
                                   errors={"name": "That group is already in the queue."}), 409
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is {ticket_label(ticket)}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


# ---------------------------------------------------------------------------
# Part 6: starting data
# ---------------------------------------------------------------------------

@app.cli.command("seed")
def seed():
    """Add the starting services and a default room if they are not there yet."""
    starting = [
        ("Project Defense", "PD"),
        ("Lab Consultation", "LC"),
        ("Grade & Requirement Inquiry", "GR"),
    ]
    for name, code in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, code=code))

    if db.session.scalar(db.select(Room)) is None:
        db.session.add(Room(name="Default Room", meeting_link=MEETING_LINK))

    db.session.commit()
    print("Services and the default room are ready.")


# ===========================================================================
# STILL THE WEEK 3 CODE: the routes below use the deleted TICKETS and
# SERVICES lists, so they error when opened. Part 8 replaces the read
# routes (My place, staff dashboard) and Part 9 replaces the update and
# delete routes. The routes must keep existing now, because the navbar and
# the redirect after joining call url_for() on their names.
# ===========================================================================

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    abort(501)  # Part 8


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    abort(501)  # Part 8


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    abort(501)  # Part 9


@app.get("/staff")
def staff_dashboard():
    abort(501)  # Part 8


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    abort(501)  # Part 9


@app.post("/staff/call-next")
def call_next():
    abort(501)  # Part 9


@app.post("/staff/clear")
def clear_queue():
    abort(501)  # Part 9


@app.post("/staff/meeting-link")
def set_meeting_link():
    abort(501)  # Part 9


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)