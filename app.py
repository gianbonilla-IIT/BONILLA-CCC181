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



@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)

    ahead = [x for x in TICKETS
             if x["status"] == "waiting" and x["number"] < t["number"]]
    current = next((x for x in TICKETS if x["status"] == "called"), None)
    service_name = next(s["name"] for s in SERVICES if s["id"] == t["service_id"])

    return render_template("ticket.html", ticket=t, service_name=service_name,
                           ahead=ahead, current=current, meeting_link=MEETING_LINK)


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


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
