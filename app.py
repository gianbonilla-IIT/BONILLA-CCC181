import itertools
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "$H@AUL@"  # Week 11 moves this into an environment variable

# Academic Services
SERVICES = [
    {"id": 1, "name": "Project Defense", "code": "PD"},
    {"id": 2, "name": "Lab Consultation", "code": "LC"},
    {"id": 3, "name": "Grade & Requirement Inquiry", "code": "GR"},
]

# Each ticket: number, group_name, service_id, status
# status: waiting, called, served, no-show
TICKETS = [
    {
        "number": 1,
        "name": "Sherlock",
        "topic": "Minimizing Traffic by Utilizing Contemporary Solutions",
        "service_id": 1,
        "status": "served",
    },
    {
        "number": 2,
        "name": "8Eyes",
        "topic": "Utilizing Open-Source Fly Brain to Beat Simple Video Games",
        "service_id": 1,
        "status": "no-show",
    },
    {
        "number": 3,
        "name": "Media Minds",
        "topic": "Analyzing the Impact of Social Media on Student Performance",
        "service_id": 1,
        "status": "called",
    },
    {
        "number": 4,
        "name": "Tech Innovators",
        "topic": "Exploring the Potential of Quantum Computing in Data Analysis",
        "service_id": 1,
        "status": "waiting",
    },
    {
        "number": 5,
        "name": "Index",
        "topic": "Developing a Mobile App for Efficient Campus Navigation",
        "service_id": 1,
        "status": "waiting",
    },
    {
        "number": 6,
        "name": "LightLLC",
        "topic": "Investigating the Use of Light-Based Communication for High-Speed Data Transfer",
        "service_id": 1,
        "status": "waiting",
    },
    {
        "number": 7,
        "name": "GymSolutions",
        "topic": "Designing a Smart Fitness App to Optimize Workout Routines",
        "service_id": 1,
        "status": "waiting",
    },
    {
        "number": 8,
        "name": "Thrift&Trade",
        "topic": "Creating a Sustainable E-commerce Platform for Second-Hand Goods",
        "service_id": 1,
        "status": "waiting",
    }
]

_ticket_numbers = itertools.count(max((t["number"] for t in TICKETS), default=0) + 1)



MEETING_LINK = "https://meet.google.com/abc-defg-hij"  # Provided by the teacher

@app.template_global()
def ticket_label(t):
    code = next((s["code"] for s in SERVICES if s["id"] == t["service_id"]), "")
    return f"{code}{t['number']:02d}"

@app.route("/")
def index():
    return render_template("index.html")

def _queue_context(t):
    """Everything My place needs to know about the line, from ticket t's point of view.

    Returns (ahead_count, upcoming, waiting_count, current):
      ahead_count   - waiting tickets with a lower number than t (people ahead of you)
      upcoming      - the first 4 waiting tickets in the whole line (may include t itself)
      waiting_count - how many tickets are waiting in total
      current       - the ticket currently being called, or None
    """
    waiting = sorted((x for x in TICKETS if x["status"] == "waiting"),
                     key=lambda x: x["number"])
    ahead_count = sum(1 for x in waiting if x["number"] < t["number"])
    upcoming = waiting[:4]
    current = next((x for x in TICKETS if x["status"] == "called"), None)
    return ahead_count, upcoming, len(waiting), current

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    ahead_count, upcoming, waiting_count, current = _queue_context(t)
    service_name = next(s["name"] for s in SERVICES if s["id"] == t["service_id"])

    return render_template("ticket.html", ticket=t, service_name=service_name,
                           ahead_count=ahead_count, upcoming=upcoming,
                           waiting_count=waiting_count, current=current,
                           meeting_link=MEETING_LINK)

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead_count, upcoming, waiting_count, current = _queue_context(t)
    return {
        "status": t["status"],
        "ahead": ahead_count,
        "waiting": waiting_count,
        "upcoming": [{"label": ticket_label(x), "mine": x["number"] == t["number"]}
                     for x in upcoming],
        "current": ticket_label(current) if current else None,
    }

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    if t["status"] in ("waiting", "called"):
        TICKETS.remove(t)
        flash("You left the queue.", "info")
    else:
        flash("That ticket is already closed.", "warning")
    return redirect(url_for("join_form"))


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    topic = form.get("topic", "").strip()
    service_id = form.get("service_id", type=int)

    errors = {}
    if not name:
        errors["name"] = "Enter your name or group name."
    elif len(name) > 60:
        errors["name"] = "Keep the name under 60 characters."
    if not topic:
        errors["topic"] = "Enter your topic or what you need help with."
    elif len(topic) > 150:
        errors["topic"] = "Keep the topic under 150 characters."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = next(_ticket_numbers)
    TICKETS.append({
        "number": number,
        "name": name,
        "topic": topic,
        "service_id": service_id,
        "status": "waiting",
    })
    flash(f"You joined the queue. Your ticket is {ticket_label(TICKETS[-1])}.", "success")
    return redirect(url_for("ticket", ticket_id=number))


def _back_to_dashboard():
    """Redirect to the dashboard, keeping the service filter if one was active."""
    sid = request.form.get("service_id", type=int)
    return redirect(url_for("staff_dashboard", service_id=sid))

def _someone_is_called():
    return any(t["status"] == "called" for t in TICKETS)

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    rows = TICKETS
    if service_id:
        rows = [t for t in TICKETS if t["service_id"] == service_id]
    names = {s["id"]: s["name"] for s in SERVICES}
    return render_template("staff.html", rows=rows, services=SERVICES, names=names,
                           selected=service_id, meeting_link=MEETING_LINK,
                           has_called=_someone_is_called(),
                           called=next((t for t in TICKETS if t["status"] == "called"), None))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    label = ticket_label(t)

    if action == "delete":
        TICKETS.remove(t)
        flash(f"Ticket {label} deleted.", "info")
    else:
        new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
        if new_status is None:
            abort(404)
        if action == "no-show" and t["status"] != "called":
            flash("Only the ticket currently being called can be marked no-show.", "warning")
            return _back_to_dashboard()
        if action == "call" and _someone_is_called():
            flash("Serve or mark the current ticket first.", "warning")
            return _back_to_dashboard()
        t["status"] = new_status
        flash(f"Ticket {label} marked {new_status}.", "info")
    return _back_to_dashboard()


@app.post("/staff/call-next")
def call_next():
    if _someone_is_called():
        flash("Serve or mark the current ticket first.", "warning")
        return _back_to_dashboard()

    sid = request.form.get("service_id", type=int)
    nxt = next(
        (
            t
            for t in TICKETS
            if t["status"] == "waiting"
            and (not sid or t["service_id"] == sid)
        ),
        None,
    )
    if nxt:
        nxt["status"] = "called"
        flash(f"Now calling {ticket_label(nxt)}: {nxt['name']}.", "success")
    else:
        flash("No one is waiting.", "info")
    return _back_to_dashboard()


@app.post("/staff/clear")
def clear_queue():
    TICKETS.clear()
    flash("The queue was cleared.", "info")
    return redirect(url_for("staff_dashboard"))


@app.post("/staff/meeting-link")
def set_meeting_link():
    global MEETING_LINK
    link = request.form.get("meeting_link", "").strip()
    if not link.startswith(("https://", "http://")):
        flash("Enter a full link starting with https://", "danger")
    else:
        MEETING_LINK = link
        flash("Meeting link saved. Called students will see a Join the call button.", "success")
    return redirect(url_for("staff_dashboard"))


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)