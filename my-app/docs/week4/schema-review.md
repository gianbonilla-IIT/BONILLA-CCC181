# ClassQ schema self-review (Week 4)

I reviewed [`schema.md`](schema.md) as if someone else had drawn it, using the six questions from the assignment. The changes below are already applied to `schema.md`, `classq.dbml` and the ERD.

---

## Question 1: Coverage

Every requirement with **Stores data? = Yes** and still planned has a table or column. I also checked each Week 3 persona task to verify the coverage:

| Persona task | Data it needs | Where |
| --- | --- | --- |
| Marcus: join with group name, topic and service | name, topic, service | `tickets.group_name`, `tickets.topic`, `tickets.service_id` |
| Marcus: see his place and status | status, order of joining | `tickets.status`, `tickets.created_at` |
| Marcus: open the call when called | meeting link | `rooms.meeting_link`, reached through `tickets.room_id` |
| Marcus: leave the queue | a "left" state | `tickets.status` |
| Sir Bustos: view the queue in order of arrival | joining time | `tickets.created_at` |
| Sir Bustos: call the next group | status | `tickets.status` |
| Sir Bustos: mark served or no-show | status | `tickets.status` |
| Sir Bustos: manage services and the meeting link | service fields, link | `services.*`, `rooms.meeting_link` |

## Question 2: One fact in one place

A service's name and code exist only in `services`, and the meeting link only in `rooms`. A group's name and topic are repeated on every ticket the group creates, **on purpose**, because they describe each visit and can differ every time. I found no other duplicates.

## Question 3: Facts, not results

There is no stored position or "people ahead" count. They are computed from `status` and `created_at` when the page is built.

## Question 4: Bad data

| Mistake a persona could make | What stops it |
| --- | --- |
| Marcus taps *Enter Queue* twice, or opens a second tab | The disabled button (Week 3) **and** the unique index on active group names (entry 3) |
| Leaves the name blank, or types only spaces | `CHECK (length(trim(group_name)) > 0)`, plus Flask validation |
| Types a topic far too long | `varchar(150)` |
| Picks the wrong service | **Nothing in the database can know the intent.** The foreign key only proves the service exists. The disabled "Choose Service..." option and the service shown on his ticket let him notice it. |
| Sir Bustos saves a meeting link with a typo such as `meet.google.com/abc` | `CHECK (meeting_link ~ '^https?://')` catches a missing `http(s)://` but not a wrong address |
| Two services with the same name or code | `UNIQUE` on `services.name` and `services.code` |
| A ticket gets a status the app does not know | `CHECK (status IN (...))` |

## Question 5: Deletes

All foreign keys are `RESTRICT`, on purpose: a service or room that has tickets cannot be removed, so old tickets cannot lose their parent. But the *app* can still erase history by deleting tickets (entry 4).

## Question 6: Types

Every moment in time is a `timestamptz`. *Active* is a `boolean`, and nothing numeric is stored as text. The status is text, but a CHECK limits it to five values.

---

## Entries

### Entry 1: Coverage

> **Works well:** The nouns table traced every *Stores data? = Yes* requirement to a table or column, so I could see which table each feature writes to. <br>
> **Problem:** `services.code` (the PD, LC, GR prefix in ticket labels) had no FR requirement behind it.<br>
> **Change:** Added **FR-11** to `requirements.md` and to the nouns table in `schema.md`. The column stays.

### Entry 2: Columns for a dropped requirement

> **Works well:** Positions and counts are computed, never stored, so they cannot go out of date when someone leaves the line. <br>
> **Problem:** My first draft stored `services.avg_minutes`, `tickets.called_at` and `tickets.finished_at`, and a CHECK to keep them in step with `status`. All of them existed only for the estimated countdown (FR-07), which I then dropped. Nothing would ever read them. Found by questions 1 and 3. <br>
> **Change:** Removed the three columns and the status/time CHECK from `schema.md` and `classq.dbml`. `status` alone says where a ticket is. If I ever bring back the countdown, I will add the columns with a migration, which is the safe way to change a table that already holds data.

### Entry 3: Double tap

> **Works well:** CHECKs on the group name, topic, meeting link and status stop the empty or impossible values my personas are most likely to type. <br>
> **Problem:** Dropping the email in Part 2 also dropped my protection against the same person joining twice. The Week 3 disabled button only works in the browser, so a second tab or a retry could still create two tickets. Found by question 4. <br>
> **Change:** Added the partial unique index `ux_tickets_active_group_name` (`UNIQUE (room_id, lower(group_name)) WHERE status IN ('waiting', 'called')`). A group name can only be in line once at a time, and it is free again as soon as its ticket is finished. The trade-off is that two real groups with the same name cannot be in line together, which I accept, since the teacher could not tell them apart anyway. Flask will show "That group is already in the queue." when it happens.

### Entry 4: Deletes that destroy history

> **Works well:** `RESTRICT` on every foreign key means a service or room that has tickets cannot be removed by mistake, so staff reports keep their data. <br>
> **Problem:** The delete rules protect the *parents*, but the app deletes the *children*. **Delete** (FR-10) and Week 3's **Clear Queue** both erase tickets, including served and no-show ones that later reports could need. Found by question 5. <br>
> **Change:** I kept the schema as it is. FR-10 stays, because it is for mistaken and test tickets and already asks for confirmation. **Clear Queue** changes in Part 9 to remove only tickets still *waiting* or *called*, so finished tickets stay as the session record, and its confirm text will say so.