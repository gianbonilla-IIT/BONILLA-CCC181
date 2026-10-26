# Proposed Application: ClassQ

| | |
|---|---|
| **Student name** | Bonilla, Gian Christian |
| **Section** | CS3A |
| **GitHub username** | gianbonilla-IIT |
| **Date submitted** | 2026-10-26 |

---

## 1. Problem Statement

Teachers spend valuable time on communicating with students and managing various apps when prompted to enter 1-on-1 meeting calls.

### 1.1 Background

Online modalities for academic purposes have become more accepted in these contemporary times. In some situations, teachers would opt to hold 1-on-1 meeting calls to a student or a group of students, with more waiting in the background under a time constraint. This is done for various reasons, but most notably for presentation defenses.  

In my experience, a professor of mine from last semester conducted these calls by letting students manually inputting their group names in google docs for the queueing. Moreover, when their turn is up, the professor directly messaged our group if we are ready; afterwards, we students then edit the google docs when our turn is done to signify progress. 

### 1.2 Evidence from research

| Method | Who / where | Key finding |
|---|---|---|
| Interview | 3rd year student | The interviewee noted that he spent valuable time periodically checking the queueing documents so that he'll know when he is up. He shared that he gets anxious when the updates stop for a certain amount of time, overthinking if the group that is done didn't bother to update the document. |
| Interview | grade 12 teacher | The interviewee shared that managing 1-on-1 calls as a teacher demands a lot of patience with current solutions.|
| Observation | Discord class group, last semester, June 2026 | both teachers and students are complying, however the methods are inefficient |

### 1.3 Point-of-view (POV) statement

Teachers and students need an application that automates the queueing and notifying system because current solutions are inefficient.

### 1.4 "How might we…?" question

How might we incorporate a queueing system that benefits both teachers and students, enough to outweigh the con that this is simply one other app that will be added to their workflow?

### 1.5 Self-check

- [x] Names a real user group
- [x] States a need, not a feature
- [x] Rests on an insight from research
- [x] Is narrow enough to act on and open enough to allow different ideas

---

## 2. Target-User Profile

### 2.1 Primary persona

> Every detail should trace back to your research. Label the persona as fictional if it combines several real people.

| | |
|---|---|
| **Name, age** | Marcus, 21 (Fictional but based on 3rd-year CS student interview) |
| **Role / background** | 3rd-year undergraduate student enrolled in heavy project-based coursework with recurring capstone and lab defense schedules |
| **Goals** | Know his group’s exact place and estimated call time in queue; prepare and transition smoothly into 1-on-1 defense calls without constant manual tab-switching |
| **Frustrations / pain points** | Anxiety and dead-time caused by stale, manual Google Docs; fear of missing the call if a previous group finishes early; constantly refreshing and messaging classmates |
| **Context of use** | Laptop or smartphone connected via residential Wi-Fi or mobile data; multi-tasking across Discord, slide presentations, and video call platforms (Google Meet/Zoom) |
| **Accessibility considerations** | Clear visual hierarchy, high-contrast queue status badges (Waiting, Up Next, In Progress), audio/browser push pings for turn alerts |
| **Current workaround** | Keeping a shared Google Doc or spreadsheet open side-by-side, periodically refreshing and watching chat channels (Discord/Messenger) for manual call-outs |

### 2.2 User groups and stakeholders

| Group | Who | Relationship to the app |
|---|---|---|
| Primary users | College/High school students (individual or group leaders) | Uses the app to join queues, check real-time wait times, and receive automatic notifications when called |
| Secondary users | Teachers, professors, and lab instructors | Uses the app to host sessions, advance the queue with a single click, trigger automated pings, and track call elapsed time |
| Stakeholders | School IT administration, academic department chairs | Evaluates data privacy compliance (RA 10173), student productivity, and ease of adoption into existing LMS workflows |

### 2.3 Organizational needs

- Data Privacy & Minimal Data Collection: Compliance with the Data Privacy Act of 2012 (RA 10173). The system must only collect temporary identifying labels (e.g., student/group name and school email or session token) and purge transient queue records after the session concludes.
- Zero-Friction Adoption & Cost Efficiency: Must operate under free-tier infrastructure without requiring paid institutional software licenses or mandatory app store downloads.
- Balancing App Fatigue vs. Single-Purpose Simplicity: To prevent pushback against introducing "yet another app," the solution must not require formal account registration for students—a lightweight join link or room code with real-time browser notifications must suffice.

---

## 3. Proposed Application

### 3.1 Concept

ClassQ is a lightweight, real-time web application engineered to automate queue management and turn notifications for academic 1-on-1 and group consultations or defense calls. Teachers create a dedicated queue room, generate a shareable link or code, and manage turns with a single "Call Next" button. Students join the room via browser, see their live standing in line with an estimated wait time, and receive instant sound or push alerts when their turn arrives. By replacing manually edited shared documents and fragmented direct messages, ClassQ eliminates waiting anxiety and administrative overhead.

### 3.2 Value proposition

For **educators and students** who **conduct 1-on-1 defense sessions and consultation calls**, **ClassQ** is a **lightweight, real-time queue management web app** that **automates queue advancement and instant turn notifications**. Unlike **manually updated Google Docs and Discord/Messenger direct chats**, it **provides live synchronization and automated alerts without requiring complex software installation or manual document maintenance**.

### 3.3 Value Proposition Canvas

| User side | Product side |
|---|---|
| **Jobs:** [ ] | **Features:** [ ] |
| **Pains:** [ ] | **Pain relievers:** [ ] |
| **Gains:** [ ] | **Gain creators:** [ ] |

### 3.4 Existing applications (from your application analysis)

| Existing app | What it does well | Where it falls short | How your app differs |
|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] |

### 3.5 Technology choice

> Choose the simplest technology that delivers the value proposition. "No emerging technology needed" is an acceptable, defensible answer.

**Options considered:** [e.g., PWA, native mobile app, AI/LLM feature, IoT sensor, cloud/serverless]

**Weighted decision matrix** (scores 1–5, higher is better):

| Option | Solves the problem ×3 | Team skills ×2 | Cost ×2 | Privacy ×2 | Time to MVP ×1 | Total /50 |
|---|---|---|---|---|---|---|
| [Option A] | | | | | | |
| [Option B] | | | | | | |
| [Option C] | | | | | | |

**Chosen technology and rationale:** [Which option you chose, and which pain or requirement it addresses.]

---

## 4. Preliminary Requirements

### 4.1 Functional requirements (user stories)

> Format: As a **[user]**, I want **[action]** so that **[benefit]**.

| ID | User story | Priority (MoSCoW) |
|---|---|---|
| FR-01 | As a [ ], I want [ ] so that [ ]. | Must |
| FR-02 | As a [ ], I want [ ] so that [ ]. | Must |
| FR-03 | As a [ ], I want [ ] so that [ ]. | Should |
| FR-04 | As a [ ], I want [ ] so that [ ]. | Could |
| FR-05 | As a [ ], I want [ ] so that [ ]. | Won't (this time) |

### 4.2 Non-functional requirements

> Make each one measurable: "fast" is not a requirement; "updates within 5 seconds" is.

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | [ ] |
| NFR-02 | Usability | [ ] |
| NFR-03 | Security / privacy | [ ] |
| NFR-04 | Compatibility | [ ] |

### 4.3 MoSCoW summary

> Test for a Must: if the app still solves your POV statement without this feature, it is not a Must. Keep the Must list short.

- **Must have:** [ ]
- **Should have:** [ ]
- **Could have:** [ ]
- **Won't have (this time):** [ ]

---

## 5. Minimum Viable Product (MVP)

> The smallest version of the app that still solves the core problem for your primary persona. It is the scope you commit to finishing this semester.

### 5.1 MVP features

[List the features in the MVP; they should match your Must list.]

1. [ ]
2. [ ]
3. [ ]

### 5.2 Out of scope

- [Feature or capability not included, and why]
- [ ]

### 5.3 Constraints and assumptions

- **Constraints:** [e.g., one semester, free hosting tier, solo developer]
- **Assumptions:** [e.g., users have a smartphone with mobile data]

### 5.4 Feasibility check (TELOS)

| Dimension | Key question | Your assessment |
|---|---|---|
| Technical | Can I build it with my skills and tools? | [ ] |
| Economic | Do the benefits justify the costs? | [ ] |
| Legal | Does it comply with law and policy (e.g., RA 10173)? | [ ] |
| Operational | Will people use it, and can it be run? | [ ] |
| Schedule | Can I deliver the MVP this semester? | [ ] |

**Verdict:** [Feasible / feasible if … / not feasible, with a short reason]

---

## Submission Checklist

- [ ] File saved as `activities/proposed-application/README.md` in my CCC181 repository
- [ ] All `[bracketed placeholders]` replaced and guidance blockquotes removed
- [ ] Sections 1–5 complete
- [ ] Images (if any) placed in `images/` and displaying correctly on GitHub
