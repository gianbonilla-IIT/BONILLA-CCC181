# ClassQ Requirements

**Setting:** Academic defenses and 1-on-1 instructor consultations in university and secondary school courses.  
**People who wait:** Marcus (Undergraduate CS Student managing heavy project-based coursework; detailed in [`docs/week3/personas.md`](week3/personas.md)).  
**People who serve:** Sir Bustos (Computer Science Instructor handling laboratory sections and capstone defenses; detailed in [`docs/week3/personas.md`](week3/personas.md)).  

**Problem statement:** An undergraduate student juggling group presentations needs a way to join an active queue track without manual sign-in sheets and monitor their exact standing in real time, because manual updates stall and stepping away causes them to miss their presentation call.

---

## 1b. Functional Requirements

| ID | Requirement | Priority | Stores data? | Status |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 ★ | As a teacher, I want to create a queue room with an active meeting link so that students know where to enter when called. | Must | **Yes** | Built (Week 3) |
| FR-02 ★ | As a student, I want to enter my identification details (name, topic details, service option) to join the queue without creating an account. | Must | **Yes** | Built (Week 3) |
| FR-03 | As a student, I want to see a live-updating dashboard showing my current turn status and position in line. | Must | **Yes** | Built (Week 3) |
| FR-04 | As a teacher, I want a single "Call Next" control to advance the queue and call the next group. | Must | **Yes** | Built (Week 3) |
| FR-05 | As a student, I want real-time status alerts and dynamic view updates on my ticket status page. | Should | **Yes** | Built (Week 3) |
| FR-06 | As a student or teacher, I want the ability to leave the queue or mark tickets as served or no-show. | Should | **Yes** | Built (Week 3) |
| FR-07 | As a student and teacher, I want an estimated countdown timer based on average call duration so that we can plan accordingly. | Won't | **Yes** | Dropped |
| FR-08 | As a teacher, I want to export session queue history and attendance logs to CSV so that I have records for grading. | Won't  | **Yes** | Dropped |
| FR-09 ★ | As a teacher, I want to manage service tracks (add, rename, and toggle active/inactive). | Must | **Yes** | This week |
| FR-10 | As a teacher, I want to permanently delete mistaken or test tickets from the dashboard. | Must | **Yes** | This week |
| FR-11 | Every ticket label starts with its service code | Should | **Yes** | Built (Week 3) |

*Note: Requirements marked with ★ denote setting-specific features tailored to academic consultation queues.*

---

## 1c. Non-Functional Requirements

| ID | Requirement | Category | Priority |
| :--- | :--- | :--- | :--- |
| NFR-01 | Queue updates and ticket state must propagate to connected clients within 1.5 seconds of a state change. | Performance | Must |
| NFR-02 | Students must be able to join the queue with minimal friction without requiring account registration or password setup. | Usability | Must |
| NFR-03 | Transient queue records and environment secrets (passwords, keys) must strictly comply with data minimization and never be committed to Git history. | Security / Privacy | Must |
| NFR-04 | The application interface must render seamlessly on desktop and mobile web browsers, scoring 95+ on Lighthouse accessibility checks. | Compatibility / Accessibility | Must |
| NFR-05 | No ticket or queue state is lost when the Flask server or PostgreSQL database restarts. | Reliability | Must |
| NFR-06 | Concurrent queue submissions can never produce duplicate ticket primary keys or sequence numbers in the database. | Data Integrity | Must |

---

## 1d. MVP & Out of Scope

### Minimum Viable Product (MVP)
The MVP consists of **FR-01, FR-02, FR-03, FR-04, FR-05, FR-06, FR-09, and FR-10**. This selection represents the absolute minimum functionality required for an instructor to host structured consultation sessions and defenses without losing line state across restarts or risking duplicate tickets.

### Out of Scope (This Semester)
1. **FR-07 (Estimated Countdown Timer):**  It adds uneccesary complexity to my queueing app.
2. **FR-08 (CSV Export & Session Grading Logs):** Session reporting will not export directly to downloadable CSV files this semester.
3. **Multi-Tenant User Authentication & OAuth:** Students will not register permanent accounts or log in via Google OAuth; identity relies on the ticket itself, with no email or personal contact details collected.

---

## 1e. Requirement Verification Feedback

The requirement list was reviewed with **Al** (CSM student; non-CCC181 peer tester).

1. Is anything missing that you would need?
> "Honestly, the main thing missing was clarity on what to put in the 'Topic' field. When I joined the line, I wasn't sure if it meant my full research paper title or just a short summary of my lab issue. Depending on whether I'm queuing for a defense, a code debugging session, or a grade check, that changes. Having dynamic hints or placeholders that match the selected service track makes a big difference so students don't hesitate at the form."

2. Is anything here wrong, or not important to you?
> "Nothing stands out as wrong, but some of the potential extra features like high-contrast outdoor viewing modes or fancy LMS grade exports aren't really important to me right now. When we're waiting outside the defense room, all we care about is zero-friction joining without creating yet another account, and knowing our exact standing so we don't miss our turn."

3. Which three matter most to you?
> "The three that matter most to me as a student are: <br> (1) Joining quickly with just our name, topic, and service without forcing us to register passwords or create accounts.<br> (2) Seeing our ticket number, live status, and exact count of groups ahead so we know when to get ready. <br> (3) Getting immediate status updates and having the Google Meet/Zoom link show up right on our ticket the second Sir Bustos calls our group."

| Who (role only) | What they said | What I changed |
| :--- | :--- | :--- |
| Student (Consultation user) | "When I joined the queue, I wasn't sure if 'Topic' meant my full research paper title or just a short summary, so I hesitated." | Clarified the topic field requirement (FR-02) and placeholder. |
