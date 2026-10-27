# Part 10: Usability test, one fix, and submission

## 10a. Test with a real user (asynchronous)
- **Participant:** "J.R." (3rd-year college student from another department; matches the **Marcus** waiting student persona; not enrolled in CCC181).
- **Consent:** Verbal permission granted to observe and log notes anonymously (no face or full name recorded).
- **Device & Environment:** Tested in person using a phone connected over local Wi-Fi (`flask --app app run --debug --host 0.0.0.0`) at 375 px mobile viewport width, and switched to laptop for the staff view.

---

### Task 1: "You just arrived. Get in line for Project Defense."

- **Did they finish it?** Yes
- **About how long it took:** ~22 seconds
- **Where they hesitated, what they said, and anything that surprised you:**
  - The tester started on the `/join` screen, immediately tapped "Student/Group Name" and typed "Group 4", then typed "Capstone Proposal" under "Topic".
  - They briefly hesitated for about 3 seconds on the "Topic" field and asked aloud, *"Is this our research title or what we want to ask?"* before typing their title based on the placeholder text (`A Showcase of a Novel Algorithm`).
  - They selected "Project Defense" from the Service dropdown and tapped "Enter Queue".
  - **What surprised me:** When they tapped the `"Enter Queue"` button, he noticed within the split second it can be observed, that the button's text changed to `"Getting your ticket…"` and disabled itself. It is pretty neat that he noticed this behavior.
- **Which of your persona's "Because …, my interface must …" rules held up, and which did not:**
  - **Held up:** Marcus Rule 3 (*"Because he needs to join rapidly before defense slots fill up, the join form must require minimal inputs and zero account registration friction"*). The tester joined in under 25 seconds with no login barrier.
  - **Did not hold up / Needed refinement:** None broke, though the placeholder text carried the weight of explaining what "Topic" meant.

---

### Task 2: "How many people are ahead of you? What is your number?"

- **Did they finish it?** Yes
- **About how long it took:** ~8 seconds
- **Where they hesitated, what they said, and anything that surprised you:**
  - As soon as the `/queue/9` page loaded, the tester looked at the big `#03` (`PD03`) box at the top and initially said, *"Oh, I'm number 3—wait no, that says 'Currently entertaining'"*.
  - Their eyes moved down to `"Your ticket number is: PD09"` and the second card showing `"5 people ahead of you"`, and they answered: *"There are 5 people ahead of me, and my number is PD09"*.
  - **What surprised me:** Because `#03` (`display-1`) is much larger than the user's own ticket badge (`fs-5`), the tester's first instinct was to read the giant number as their own ticket before reading the small `"Currently entertaining:"` label above it. Also, when they wanted to switch to the Staff Dashboard for Task 3, there was no link on the ticket page (since `nav_links` is hidden on `ticket.html`).
- **Which of your persona's "Because …, my interface must …" rules held up, and which did not:**
  - **Held up:** Marcus Rule 1 (*"Because Marcus gets anxious when document updates stall, the ticket position and status badge must update automatically without requiring manual page reloads"*). The status badge and `"5 people ahead of you"` text were clear and updated live.
  - **Did not hold up / Needed refinement:** Marcus Rule 2 (*"Because he multi-tasks across presentation slides and chat apps while waiting, the interface must provide clear, prominent visual indicators..."*). Having the currently called number be giant while the student's own ticket number is a small pill badge caused a 2-second misread on first glance.

---

### Task 3: "Pretend you are the staff member. Call the next person and mark them as served."

- **Did they finish it?** Yes
- **About how long it took:** ~35 seconds
- **Where they hesitated, what they said, and anything that surprised you:**
  - Once on `/staff`, the tester wanted to call the next waiting group (`PD04: Tech Innovators`).
  - However, because `PD03 (Media Minds)` was already in the `called` state in the starter data, the bottom sticky bar showed **"No Show"** and **"Serve"** instead of **"Call Next"**, and the inline Call buttons on waiting rows were hidden.
  - The tester hesitated for ~10 seconds scanning the page and said, *"Where is the Call button? Oh, someone is already called. Let me serve Media Minds first."*
  - They clicked the big green **Serve** button at the bottom, confirmed the popup dialog, saw the big blue **Call Next** button appear, clicked **Call Next** (calling `PD04`), and then clicked **Serve** to mark `PD04` as served.
  - **What surprised me:** When the tester also tried filtering the table by service ("Project Defense") and clicked **Call Next**, the page redirected back to `/staff` with the service filter wiped out (resetting to "All Services"), and the confirmation dialog popped up on every single routine click (`"Serve ticket PD03?"`, `"Call the next ticket?"`), which the tester remarked felt repetitive for non-destructive actions.
- **Which of your persona's "Because …, my interface must …" rules held up, and which did not:**
  - **Held up:** Sir Bustos Rule 3 (*"Because he monitors grading rubrics and video calls at the same time, the queue table must present a clear, scannable overview with status tags..."*). The yellow highlight on the `called` row helped them figure out why they couldn't call a new group yet.
  - **Did not hold up / Needed refinement:** Sir Bustos Rule 1 (*"Because Sir Bustos runs tight call schedules and dislikes manual messaging, the primary 'Call Next' button must automatically notify the students waiting and update the queue"*). Having browser `confirm()` popups on routine actions (`Call Next` and `Serve`) and losing the active service filter when clicking `Call Next` added extra clicks and friction to the teacher's most frequent workflow.

---

## 10b. Make one improvement

### Problem Identified
When the staff member filters the dashboard by a specific service (e.g., `Project Defense` or `Lab Consultation`) and clicks **Call Next**, the form in `templates/staff.html` did not include `<input type="hidden" name="service_id">`, and `call_next()` in `app.py` redirected to `url_for("staff_dashboard")` instead of `_back_to_dashboard()`. This wiped out the teacher's active filter and called tickets outside the filtered service track.

### How It Was Fixed
1. **In `templates/staff.html`:** Added `<input type="hidden" name="service_id" value="{{ selected or '' }}">` inside the `call_next` POST form so the active service filter is submitted.
2. **In `app.py`:** Updated `call_next()` to filter waiting tickets by `service_id` when a filter is active and return `_back_to_dashboard()` so the staff member stays on their filtered view.

### Verification After Fix
Filtered `/staff` by "Project Defense", served ticket `PD03`, and clicked **Call Next**. The dashboard remained filtered to "Project Defense" and called `PD04` without losing state.

### BEFORE:
![filter goes back to "All Services" upon calling the next ticket](screenshots\section-10b-before.png)

### AFTER:
![filter remains to current service selected upon calling the next ticket](screenshots\section-10b-after.png)