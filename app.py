"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# Academic Consultation / Defense Services
SERVICES = [
    {"id": 1, "name": "Capstone / Project Defense"},
    {"id": 2, "name": "Lab Consultation"},
    {"id": 3, "name": "Grade & Requirement Inquiry"},
]

# Each ticket: number, group_name, student_id, service_id, meeting_link, status
# status: waiting, called, served, no-show
TICKETS = [
    {
        "number": 1,
        "name": "Group 1 - Alpha",
        "student_id": "2023-0001",
        "service_id": 1,
        "meeting_link": "https://meet.google.com/abc-defg-hij",
        "status": "waiting",
    },
    {
        "number": 2,
        "name": "Marcus (Solo Defense)",
        "student_id": "2023-0452",
        "service_id": 1,
        "meeting_link": "https://meet.google.com/abc-defg-hij",
        "status": "waiting",
    },
]


@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number


@app.route("/join", methods=["GET", "POST"])
def join():
    # GET: show the empty form. POST: the form was submitted.
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("join.html", error="Please enter your name.")

        number = TICKETS[-1]["number"] + 1 if TICKETS else 1
        TICKETS.append({"number": number, "name": name})
        # Redirect after POST so refreshing the page doesn't join twice.
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
