# Design Self-Review: ClassQ Wireframes

This self-review evaluates the ClassQ wireframe designs against our primary personas, Marcus (student waiting) and Sir Bustos (teacher acting as staff).

---

## Screen 1: Join the Queue (`/join`)

### Core Questions Review
1. **Can my persona tell what to do on this screen within 5 seconds?**  
   Yes; the screen features a prominent centered card titled "Join Queue" with only three visible inputs (Student/Group Name, Topic, and Service Category) and a clear "Enter Queue" button.
2. **Is the ticket status always visible where the person needs it?**  
   Not applicable yet on this screen; ticket status only exists once the student submits the form and transitions to the ticket status screen.
3. **Do the words match what people in my setting actually say? (For example "window" or "counter", "number" or "ticket".)**  
   Yes; the copy uses academic defense terms like "Student/Group Name", "Topic", and "Project Defense" rather than generic clinic terminology like "Patient", "Counter", or "Doctor".
4. **Is the action the staff member does most often the easiest one to reach?**  
   Yes; staff members opening this page have a dedicated, high-contrast "Staff Dashboard" button pinned directly in the navigation bar to jump straight to their panel.
5. **Does the phone version still show the most important thing first?**  
   Yes; on mobile (`join-phone.png`), extraneous margins collapse so that the "Join Queue" card, form fields, and "Enter Queue" button occupy the prime viewport area above the fold.
6. **Which of my "Because …, my interface must …" rules does this screen follow, and which does it break?**  
   * *Follows:* Rule 3 ("Because he needs to join rapidly before defense slots fill up, the join form must require minimal inputs and zero account registration friction"). The form only asks for name, topic, and service track.  
   * *Breaks / Needs adjustment:* None broken, though client-side submission prevention is needed so rapid double-clicks do not generate accidental multiple tickets.

### Evaluation
* **Works well:** The single-action card, lack of mandatory login, and academic-specific topic input allow students to enter the queue within seconds without cognitive overload.
* **Problem:** If a student with an unstable Wi-Fi connection clicks "Enter Queue" multiple times, the server could create duplicate tickets for the same group. Additionally, an unvalidated default in the dropdown could result in accidental submissions under the wrong track.
* **Change:** Implement client-side submit-disabling on click (Part 8a) and ensure the dropdown includes a disabled instructional default option (`<option value="">Choose Service...</option>`) enforced by server-side validation.

---

## Screen 2: My Place (`/queue/<id>`)

### Core Questions Review
1. **Can my persona tell what to do on this screen within 5 seconds?**  
   Yes; Marcus immediately sees the huge "Currently entertaining: #03" counter, the queue progress tickets, and his personal ticket number (#08).
2. **Is the ticket status always visible where the person needs it?**  
   Yes; the lower card clearly highlights the user's personal ticket status in a dedicated badge (e.g., `status: waiting`) right above the "Leave Queue" button.
3. **Do the words match what people in my setting actually say? (For example "window" or "counter", "number" or "ticket".)**  
   Yes; the labels say "Currently entertaining", "Upcoming tickets", "Your ticket number", and "Leave Queue" rather than clinic or retail terms.
4. **Is the action the staff member does most often the easiest one to reach?**  
   Not applicable on this view; the staff dashboard link is intentionally omitted from this screen so students waiting cannot inadvertently stumble into the teacher's grading panel.
5. **Does the phone version still show the most important thing first?**  
   Yes; on mobile (`ticket-phone.png`), the large active ticket counter dominates the top half of the screen, followed by upcoming tickets and Marcus's status, ensuring instant status reading on small screens.
6. **Which of my "Because …, my interface must …" rules does this screen follow, and which does it break?**  
   * *Follows:* Rule 1 ("Because Marcus gets anxious when document updates stall, the ticket position and status badge must update automatically without requiring manual page reloads") and Rule 2 ("Because he multi-tasks across slides and chat apps, the interface must provide clear, prominent visual indicators when his status changes").  
   * *Breaks / Needs adjustment:* On a purely static wireframe, a student does not know if the page has stalled without background polling.

### Evaluation
* **Works well:** The visual separation between "Currently entertaining" and personal ticket status keeps Marcus aware of defense session progress without exposing other students' private details.
* **Problem:** Marcus keeps the tab open in the background while reviewing presentation slides; if the page requires manual browser refreshes, his anxiety over whether the queue is moving will persist.
* **Change:** Add background polling via JavaScript (`/queue/<id>/status`) every 10 seconds to update the active ticket counter and status badge dynamically without full page reloads, paired with an `aria-live="polite"` region for accessibility.

---

## Screen 3: Staff Dashboard (`/staff`)

### Core Questions Review
1. **Can my persona tell what to do on this screen within 5 seconds?**  
   Yes; Sir Bustos immediately sees the prominent green "Call Next" button anchored under the table, with the current defense session highlighted in the list.
2. **Is the ticket status always visible where the person needs it?**  
   Yes; every row has a high-contrast badge (`served`, `no show`, `called`, `waiting`), and the active ticket is styled with a distinct yellow highlight row.
3. **Do the words match what people in my setting actually say? (For example "window" or "counter", "number" or "ticket".)**  
   Yes; column headers read "Ticket #", "Name", "Topic", "Status", and "Actions", representing student project defense evaluations.
4. **Is the action the staff member does most often the easiest one to reach?**  
   Yes; "Call Next" is the largest and most prominent interactive button on the screen, positioned for rapid one-click queue progression.
5. **Does the phone version still show the most important thing first?**  
   Yes; on mobile (`staff-phone.png`), the large "Call Next" action remains immediately accessible, while wider columns collapse and provide an info icon (`ℹ`) to view project topics without breaking screen width.
6. **Which of my "Because …, my interface must …" rules does this screen follow, and which does it break?**  
   * *Follows:* Rule 1 ("Because the instructor runs tight call schedules, the primary Call Next button must be prominently placed for instant one-click action") and Rule 2 ("Because students sometimes drop or fail to connect, rows must offer direct action buttons").  
   * *Breaks / Needs adjustment:* Destructive actions (like "Clear Queue" or deleting a ticket) are currently accessible with single clicks on the wireframe, risking accidental session loss.

### Evaluation
* **Works well:** The dedicated "Call Next" button advances the queue in one action (marking the previous ticket served and the next called), perfectly matching the back-to-back defense workflow.
* **Problem:** Single-click destructive actions (trash icon, "Clear Queue") could accidentally wipe active student tickets during fast-paced evaluation sessions.
* **Change:** Wrap line clearances and ticket deletions in confirmation dialogs (`confirm()`), and process all state modifications using strict HTTP POST requests with descriptive `aria-label` tags for screen reader accessibility.