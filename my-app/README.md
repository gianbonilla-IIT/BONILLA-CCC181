# ClassQ

ClassQ is a lightweight real-time queue management system tailored for academic defenses and 1-on-1 consultation sessions. It automates student turn-tracking and alerts, eliminating idle anxiety and the manual overhead of updating spreadsheets and shared documents.

## Project structure

```
my-app/
    ├── .gitignore
    ├── README.md
    ├── app.py
    ├── docs/
    │   ├── week1/
    │   │   ├── proposal.md
    │   │   └── proposal.pdf
    │   └── week3/
    │       ├── accessibility.md
    │       ├── feedback.md
    │       ├── persona-imgs/
    │       │   ├── persona-1-stock.png
    │       │   └── persona-2-stock.png
    │       ├── personas.md
    │       ├── report.md
    │       ├── screenshots/
    │       │   ├── lighthouse-join.png
    │       │   ├── lighthouse-queue.png
    │       │   ├── lighthouse-staff.png
    │       │   ├── nomouse-test1.png
    │       │   ├── nomouse-test2.png
    │       │   ├── section-10b-after.png
    │       │   └── section-10b-before.png
    │       ├── usability-test.md
    │       └── wireframes/
    │           ├── join-laptop.png
    │           ├── join-phone.png
    │           ├── staff-laptop.png
    │           ├── staff-phone.png
    │           ├── ticket-laptop.png
    │           └── ticket-phone.png
    ├── requirements.txt
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   ├── js/
    │   │   └── main.js
    │   └── logo.png
    └── templates/
        ├── _badges.html
        ├── base.html
        ├── index.html
        ├── join.html
        ├── staff.html
        └── ticket.html
```

## Routes

| URL | Method | View function | What it does |
|---|---|---|---|
| `/` | `GET` | `index()` | Landing page with a call-to-action to join the queue |
| `/join` | `GET`, `POST` | `join_form()`, `join()` | Student form to enter group name, topic, and service track |
| `/queue/<int:ticket_id>` | `GET` | `ticket()` | Live student ticket status page ("My place") |
| `/queue/<int:ticket_id>/status.json` | `GET` | `ticket_status()` | JSON endpoint polled every 5s for live ticket updates |
| `/queue/<int:ticket_id>/leave` | `POST` | `leave()` | Allows a waiting/called student to leave the queue |
| `/staff` | `GET` | `staff_dashboard()` | Staff dashboard with service filter, meeting link config, and queue table |
| `/staff/call-next` | `POST` | `call_next()` | Calls the next waiting ticket in line |
| `/staff/tickets/<int:ticket_id>/<action>` | `POST` | `staff_action()` | Marks a ticket as `call`, `serve`, `no-show`, or `delete` |
| `/staff/meeting-link` | `POST` | `set_meeting_link()` | Updates the active Google Meet / Zoom link for called tickets |
| `/staff/clear` | `POST` | `clear_queue()` | Clears all tickets from the queue |

# Setup Guide (CLI)

## 1. Set up the Python environment

```bash
# create (once per project)
python -m venv .venv

# activate (every new terminal)
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# install the packages
pip install -r requirements.txt
```

Your prompt shows `(.venv)` when the environment is active. Some systems use `python3` or `py` instead of `python`.
If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

If you add more packages later, record them with:

```bash
pip freeze > requirements.txt
```

## 2. Run the app

```bash
flask --app app run --debug
```

Open http://127.0.0.1:5000. With `--debug`, the server reloads every time you save a file. Never use debug mode in production.

