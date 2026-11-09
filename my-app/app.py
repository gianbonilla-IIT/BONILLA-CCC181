import os
import re
from datetime import timedelta, timezone

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func, tuple_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload

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


def all_services(active_only=True):
    """Services for a dropdown. The join form offers only active ones; staff filters list all."""
    stmt = db.select(Service).order_by(Service.id)
    if active_only:
        stmt = stmt.where(Service.active)
    return db.session.scalars(stmt).all()


def current_room():
    """ClassQ has one default room for now (created by the seed command)."""
    return db.session.scalar(db.select(Room).order_by(Room.id))


PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Nov 09, 2026 - 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %Y - %I:%M %p") if value else ""


def _waiting_in_room(room_id):
    """Waiting tickets of a room in the order they joined."""
    return (db.select(Ticket)
            .options(joinedload(Ticket.service))
            .where(Ticket.room_id == room_id, Ticket.status == "waiting")
            .order_by(Ticket.created_at, Ticket.id))


def people_ahead(t):
    """Count tickets still waiting in the same room that joined before t.
    Counted in the database, never stored. The id breaks ties between equal times."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.room_id == t.room_id,
                   Ticket.status == "waiting",
                   tuple_(Ticket.created_at, Ticket.id) < tuple_(t.created_at, t.id)))
    return db.session.scalar(stmt)


def called_ticket(room_id):
    """The ticket being called right now in a room, or None."""
    return db.session.scalar(
        db.select(Ticket)
        .options(joinedload(Ticket.service))
        .where(Ticket.room_id == room_id, Ticket.status == "called")
        .order_by(Ticket.id))


def queue_context(t):
    """Everything My place shows, from the point of view of ticket t."""
    upcoming = db.session.scalars(_waiting_in_room(t.room_id).limit(4)).all()
    waiting_count = db.session.scalar(
        db.select(func.count()).select_from(Ticket)
        .where(Ticket.room_id == t.room_id, Ticket.status == "waiting"))
    return {
        "ahead": people_ahead(t),
        "upcoming": upcoming,
        "waiting_count": waiting_count,
        "current": called_ticket(t.room_id),
    }


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


# ---------------------------------------------------------------------------
# Part 8: Read (My place and the staff dashboard) - uses the database
# ---------------------------------------------------------------------------

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ctx = queue_context(t)
    return render_template("ticket.html", ticket=t, service_name=t.service.name,
                           ahead_count=ctx["ahead"], upcoming=ctx["upcoming"],
                           waiting_count=ctx["waiting_count"], current=ctx["current"],
                           meeting_link=t.room.meeting_link)


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ctx = queue_context(t)
    return {
        "status": t.status,
        "ahead": ctx["ahead"],
        "waiting": ctx["waiting_count"],
        "upcoming": [{"label": ticket_label(x), "mine": x.id == t.id}
                     for x in ctx["upcoming"]],
        "current": ticket_label(ctx["current"]) if ctx["current"] else None,
    }


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    room = current_room()
    rows = []
    called = None
    if room is not None:
        stmt = (db.select(Ticket)
                .options(joinedload(Ticket.service))
                .where(Ticket.room_id == room.id)
                .order_by(Ticket.created_at, Ticket.id))
        if service_id:
            stmt = stmt.where(Ticket.service_id == service_id)
        rows = db.session.scalars(stmt).all()
        called = called_ticket(room.id)
    return render_template("staff.html", rows=rows, services=all_services(active_only=False),
                           selected=service_id, called=called, has_called=called is not None,
                           meeting_link=room.meeting_link if room else MEETING_LINK)


# ---------------------------------------------------------------------------
# Part 9: Update and delete
# ---------------------------------------------------------------------------

STAFF_ACTIONS = {"call": "called", "serve": "served", "no-show": "no-show"}


def _back_to_dashboard():
    """Redirect to the dashboard, keeping the service filter if one was active."""
    sid = request.form.get("service_id", type=int)
    return redirect(url_for("staff_dashboard", service_id=sid))


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status in ("waiting", "called"):
        t.status = "left"  # soft delete: the row stays, and the staff table hides it
        db.session.commit()
        flash("You left the queue.", "info")
    else:
        flash("That ticket is already closed.", "warning")
    return redirect(url_for("join_form"))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    t = db.get_or_404(Ticket, ticket_id)
    label = ticket_label(t)

    if action == "delete":
        db.session.delete(t)  # hard delete: the row is gone for good
        db.session.commit()
        flash(f"Ticket {label} deleted.", "info")
        return _back_to_dashboard()

    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    if action in ("serve", "no-show") and t.status != "called":
        flash("Only the ticket currently being called can be served or marked no-show.", "warning")
        return _back_to_dashboard()
    if action == "call":
        if t.status != "waiting":
            flash("Only a waiting ticket can be called.", "warning")
            return _back_to_dashboard()
        if called_ticket(t.room_id) is not None:
            flash("Serve or mark the current ticket first.", "warning")
            return _back_to_dashboard()

    t.status = new_status
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # the database allows only one called ticket per room
        flash("Serve or mark the current ticket first.", "warning")
        return _back_to_dashboard()
    flash(f"Ticket {label} marked {new_status}.", "info")
    return _back_to_dashboard()


@app.post("/staff/call-next")
def call_next():
    room = current_room()
    if room is None:
        flash("There is no queue room yet.", "warning")
        return redirect(url_for("staff_dashboard"))
    if called_ticket(room.id) is not None:
        flash("Serve or mark the current ticket first.", "warning")
        return redirect(url_for("staff_dashboard"))

    nxt = db.session.scalar(_waiting_in_room(room.id).limit(1))
    if nxt is None:
        flash("No one is waiting.", "info")
        return redirect(url_for("staff_dashboard"))

    nxt.status = "called"
    label = ticket_label(nxt)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # someone else called a ticket a moment earlier
        flash("Serve or mark the current ticket first.", "warning")
        return redirect(url_for("staff_dashboard"))
    flash(f"Now calling {label}: {nxt.group_name}.", "success")
    return redirect(url_for("staff_dashboard"))


@app.post("/staff/clear")
def clear_queue():
    room = current_room()
    if room is not None:
        db.session.execute(db.delete(Ticket).where(Ticket.room_id == room.id))
        db.session.commit()
    flash("The queue was cleared.", "info")
    return redirect(url_for("staff_dashboard"))


@app.post("/staff/meeting-link")
def set_meeting_link():
    link = request.form.get("meeting_link", "").strip()
    room = current_room()
    if room is None:
        flash("There is no queue room yet.", "warning")
    elif not link.startswith(("https://", "http://")) or len(link) > 300:
        flash("Enter a full link starting with https:// (up to 300 characters).", "danger")
    else:
        room.meeting_link = link
        db.session.commit()
        flash("Meeting link saved. Called students will see a Join Call button.", "success")
    return redirect(url_for("staff_dashboard"))


# ---------------------------------------------------------------------------
# Part 9: Manage services (create, read, update, delete)
# ---------------------------------------------------------------------------

@app.get("/staff/services")
def services_list():
    services = db.session.scalars(
        db.select(Service).options(selectinload(Service.tickets)).order_by(Service.id)
    ).all()
    return render_template("services.html", services=services)


@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    code = request.form.get("code", "").strip().upper()
    if not name or len(name) > 60 or not re.fullmatch(r"[A-Z]{2,4}", code):
        flash("Enter a name (up to 60 characters) and a code of 2 to 4 letters.", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name, code=code))
    try:
        db.session.commit()
        flash(f"Service \u201c{name}\u201d added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("A service with that name or code already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter a name of up to 60 characters.", "danger")
        return redirect(url_for("services_list"))
    s.name = name
    s.active = request.form.get("active") == "on"  # an unticked box is not sent at all
    try:
        db.session.commit()
        flash(f"Service \u201c{name}\u201d saved.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named \u201c{name}\u201d already exists.", "danger")
    return redirect(url_for("services_list"))


@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    if s.tickets:
        flash(f"\u201c{s.name}\u201d has tickets, so it cannot be deleted. Turn it off instead.", "danger")
        return redirect(url_for("services_list"))
    name = s.name
    db.session.delete(s)
    db.session.commit()
    flash(f"Service \u201c{name}\u201d deleted.", "warning")
    return redirect(url_for("services_list"))


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)