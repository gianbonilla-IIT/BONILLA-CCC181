# Personas: ClassQ

## Marcus, the student waiting

> "I spent valuable time periodically checking the queueing documents so that I'll know when I am up. I get anxious when the updates stop for a certain amount of time, overthinking if the group that is done didn't bother to update the document." *(interview, 3rd year student)*

| | |
| --- | --- |
| **Photo or sketch** | ![stock image of a filipino student using a computer](persona-1-stock.png) |
| **Age, role and background** | 21, 3rd-year Computer Science student, manages multiple team capstone and defense requirements under strict deadlines *(observation)* |
| **Goals** | 1. Enter the defense queue quickly without juggling multiple shared documents.<br>2. Know exact queue position and estimated turn in real time.<br>3. Focus on presentation review rather than constantly checking for updates. |
| **Frustrations** | 1. Anxiety over stale, manually edited Google Docs that stop updating *(interview)*.<br>2. Fear of being caught unprepared if an earlier group finishes fast or drops out.<br>3. Switching back and forth across Discord, slide decks, and meeting tabs while waiting *(observation)*. |
| **Devices and context** | Mid-range laptop connected via residential Wi-Fi, often monitoring Discord class channels while reviewing presentation slides simultaneously *(observation)* |
| **Tech comfort** | High; accustomed to developer tools, web applications, and collaborative platforms |
| **Accessibility needs** | High-contrast visual status badges, distinct audible pings for status changes when multi-tasking across open windows |

### Scenario

Marcus sits at his desk with his presentation deck open on one screen and Discord open on another *(observation)*. His team has their capstone defense today, and under the current process he has to keep a Google Doc open and watch for manual edits from previous groups *(interview)*. He opens ClassQ, enters his group name and student ID, selects "Capstone / Project Defense", and immediately sees his ticket number and position in line. Instead of dreading whether the document is outdated, he keeps ClassQ in a background tab knowing the browser badge and audio alert will fire when his team is called.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the defense queue with group name and student ID | Join | FR-02 |
| Monitor live position in line and ticket status | My place | FR-03 |
| Leave the queue if group defense is postponed | My place | FR-06 |

### What this means for my interface

1. Because Marcus gets anxious when document updates stall, the ticket position and status badge must update automatically without requiring manual page reloads.
2. Because he multi-tasks across presentation slides and chat apps while waiting, the interface must provide clear, prominent visual indicators (and audio pings) when his status changes to "Called".
3. Because he needs to join rapidly before defense slots fill up, the join form must require minimal inputs (name, ID, service) and zero account registration friction.

---

## Sir Morales, the teacher / staff member

> "Managing 1-on-1 calls as a teacher demands a lot of patience with current solutions." *(interview, grade 12 / secondary teacher)*

| | |
| --- | --- |
| **Photo or sketch** | ![stock image of a filipino teacher](persona-2-stock.png) |
| **Age, role and background** | 30, teacher handling project-heavy laboratory classes with 30+ students per section *(observation)* |
| **Goals** | 1. Conduct orderly 1-on-1 defense evaluations within limited class periods.<br>2. Call the next waiting student or group with a single action.<br>3. Prevent defense time from leaking into administrative chat coordination. |
| **Frustrations** | 1. Having to manually message each student or group on Discord or Messenger to ask if they are ready *(observation)*.<br>2. Dealing with dead time when students do not realize it is their turn.<br>3. Relying on students to update shared documents after their calls finish *(interview)*. |
| **Devices and context** | School-provided laptop at a desk, running video meeting software (Google Meet/Zoom) alongside a digital grading rubric and course syllabus |
| **Tech comfort** | Medium; proficient with LMS and video platforms, but dislikes complicated setups or managing multiple fragmented tools |
| **Accessibility needs** | Large, high-target action buttons ("Call Next", "Serve", "No-Show") with clear labeling that prevent accidental clicks during rapid sessions |

### Scenario

Sir Morales is conducting back-to-back project defense evaluations for her afternoon laboratory section *(observation)*. He opens the ClassQ Staff Dashboard, views the queue organized by ticket order, and clicks "Call Next" when ready for the first group. When a student fails to enter the video call after several minutes, he marks them as "No-Show" so the line automatically advances without manual messaging overhead. When the evaluation finishes, he clicks "Serve" and immediately moves to the next group in line.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| View active queue ordered by arrival time | Staff dashboard | FR-04 |
| Advance line and call the next group with one click | Staff dashboard | FR-04 |
| Mark absent groups as no-show or complete | Staff dashboard | FR-06 |

### What this means for my interface

1. Because Sir Morales runs tight call schedules and dislikes manual messaging, the primary "Call Next" button must be prominently placed at the top of the dashboard for instant one-click action.
2. Because students sometimes drop or fail to connect, each row must offer direct, unmistakable "Serve" and "No-show" buttons using clear POST actions to prevent accidental clicks.
3. Because he monitors grading rubrics and video calls at the same time, the queue table must present a clear, scannable overview with status tags rather than dense, cluttered controls.