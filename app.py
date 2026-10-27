from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable


# Academic Services
SERVICES = [
    {"id": 1, "name": "Project Defense"},
    {"id": 2, "name": "Lab Consultation"},
    {"id": 3, "name": "Grade & Requirement Inquiry"},
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
        "service_id": 2,
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

MEETING_LINK = "https://meet.google.com/abc-defg-hij"  # Provided by the teacher


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number


@app.route("/join")
def join_form():
    return render_template("join.html")


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
