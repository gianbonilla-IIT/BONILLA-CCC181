# ClassQ validation

The same rule can live in three places. **The browser** gives fast feedback to honest users, **Flask** is the real gatekeeper, and **the database** is the last line of defense against any bug. Each row below is one rule I tested by skipping the layer above it.

**Test setup:** Flask running on `http://127.0.0.1:5000`, PostgreSQL in Docker (`docker compose exec db psql -U classq`), seeded with services 1 to 3 (PD, LC, GR) and room 1, and at least one ticket in `tickets`. Commands starting with `curl.exe` were run in PowerShell.

---

## Browser layer (10a)

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Group name is limited to 60 characters (`String(60)`) | Browser | Opened `/join` and tried to type a 70-character group name | The box stops accepting characters at 60 (`maxlength="60"`) |
| Topic is limited to 150 characters (`String(150)`) | Browser | Pasted a 200-character topic into the topic box | The box stops at 150 (`maxlength="150"`) |
| Name, topic and service are required (NOT NULL columns) | Browser | Inspected the form in DevTools | `required` is on all three fields. The form has `novalidate`, so the browser does not block an empty submit and Flask shows my own messages instead. |

---

## Flask layer (10b)

Each request skips the form. Before and after the bad requests, `SELECT count(*) FROM tickets;` gave the same number.

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Group name is required | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=" -d "topic=Test" -d "service_id=1"` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| Topic is required | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "topic=" -d "service_id=1"` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| Service must exist | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "topic=Test" -d "service_id=999"` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| Group name is at most 60 characters | Flask | Same request with `name` set to 200 letters (`$long = "A" * 200`) | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| Topic is at most 150 characters | Flask | Same request with `topic` set to 200 letters | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| A switched-off service cannot be chosen | Flask | `UPDATE services SET active = false WHERE id = 2;` in psql, then `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=Test" -d "topic=Test" -d "service_id=2"`, then `UPDATE services SET active = true WHERE id = 2;` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| The same group cannot be in line twice (Flask catches the database's refusal) | Flask and database | Sent `curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=Dup Group" -d "topic=Test" -d "service_id=1"` twice, then `SELECT count(*) FROM tickets WHERE group_name = 'Dup Group';` | First: `302 FOUND`. Second: `409 CONFLICT` with "That group is already in the queue." The count is `1`. |
| Call Next is refused while a ticket is being called | Flask | With one ticket called: `curl.exe -i -X POST http://127.0.0.1:5000/staff/call-next`, then `SELECT id, status FROM tickets WHERE status = 'called';` | `302 FOUND` with the message "Serve or mark the current ticket first." Still exactly one called ticket. |
| No-show only works on the called ticket | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/staff/tickets/<id of a waiting ticket>/no-show` | `302 FOUND` with a warning message. The ticket is still `waiting`. |

---

## Database layer (10c)

Each statement was run in psql and skips Flask completely. **All of them failed with an `ERROR`.**

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| A ticket must belong to an existing service (FOREIGN KEY) | Database | `INSERT INTO tickets (room_id, service_id, group_name, topic) VALUES (1, 999, 'FK Test', 'Test');` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` |
| A ticket must belong to an existing room (FOREIGN KEY) | Database | `INSERT INTO tickets (room_id, service_id, group_name, topic) VALUES (999, 1, 'FK Test', 'Test');` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_room_id_fkey"` |
| A ticket must have a group name (NOT NULL) | Database | `INSERT INTO tickets (room_id, service_id, topic) VALUES (1, 1, 'Test');` | `ERROR: null value in column "group_name" of relation "tickets" violates not-null constraint` |
| A group name cannot be blank (CHECK `ck_tickets_group_name`) | Database | `INSERT INTO tickets (room_id, service_id, group_name, topic) VALUES (1, 1, '   ', 'Test');` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_group_name"` |
| A topic cannot be blank (CHECK `ck_tickets_topic`) | Database | `INSERT INTO tickets (room_id, service_id, group_name, topic) VALUES (1, 1, 'Check Test', '   ');` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_topic"` |
| A status must be one of the five allowed (CHECK `ck_tickets_status`) | Database | `UPDATE tickets SET status = 'lost' WHERE id = <an existing ticket id>;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| A service code must be 2 to 4 capital letters (CHECK `ck_services_code`) | Database | `INSERT INTO services (name, code) VALUES ('Test Service', 'pd');` | `ERROR: new row for relation "services" violates check constraint "ck_services_code"` |
| A meeting link must start with http:// or https:// (CHECK `ck_rooms_meeting_link`) | Database | `INSERT INTO rooms (name, meeting_link) VALUES ('Bad Room', 'meet.google.com/abc');` | `ERROR: new row for relation "rooms" violates check constraint "ck_rooms_meeting_link"` |
| Two services cannot share a name (UNIQUE) | Database | `INSERT INTO services (name, code) VALUES ('Project Defense', 'ZZ');` | `ERROR: duplicate key value violates unique constraint "services_name_key"` |
| Two services cannot share a code (UNIQUE) | Database | `INSERT INTO services (name, code) VALUES ('Another Service', 'PD');` | `ERROR: duplicate key value violates unique constraint "services_code_key"` |
| One active ticket per group name in a room (partial UNIQUE index `ux_tickets_active_group_name`) | Database | Inserted the same group name twice with the default status `waiting`: `INSERT INTO tickets (room_id, service_id, group_name, topic) VALUES (1, 1, 'Index Test', 'Test');` | First insert: `INSERT 0 1`. Second: `ERROR: duplicate key value violates unique constraint "ux_tickets_active_group_name"` |
| A finished ticket frees its group name (the index only covers active tickets) | Database | `UPDATE tickets SET status = 'served' WHERE group_name = 'Index Test';` and then repeated the insert above | The insert succeeds (`INSERT 0 1`) |
| Only one ticket can be called at a time in a room (partial UNIQUE index `ux_tickets_one_called_per_room`) | Database | With one ticket already called: `UPDATE tickets SET status = 'called' WHERE id = <id of a waiting ticket>;` | `ERROR: duplicate key value violates unique constraint "ux_tickets_one_called_per_room"` |
| A service that still has tickets cannot be deleted (ON DELETE RESTRICT) | Database | `DELETE FROM services WHERE id = 1;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` |
| A room that still has tickets cannot be deleted (ON DELETE RESTRICT) | Database | `DELETE FROM rooms WHERE id = 1;` | `ERROR: update or delete on table "rooms" violates foreign key constraint "tickets_room_id_fkey" on table "tickets"` |

**One good row, to see the defaults the database fills in:**

```sql
INSERT INTO tickets (room_id, service_id, group_name, topic)
VALUES (1, 1, 'Direct Insert', 'Checking defaults')
RETURNING id, status, created_at;
```

| What I expected | What happened |
| --- | --- |
| `status` = `waiting`, `created_at` = the current time with a time zone, `id` = a new number | Returned `status = waiting` and a `created_at` such as `2026-11-09 06:27:13+00`, with a new `id` |

*After the tests I deleted only my test rows (`Direct Insert`, `Index Test`, `Dup Group`).*

*Note: each failed insert still uses up an id number, so ticket numbers can skip. That is expected. It is how the database avoids ever giving the same number twice (NFR-06).*

---

## No SQL built from user input (10d)

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| The code never builds SQL by gluing text together | Code | `git grep -nE "f[\"'].*(SELECT\|INSERT\|UPDATE\|DELETE)" -- "*.py"` | Printed nothing |
| Input such as `' OR '1'='1` is stored as plain text, not run as SQL | Flask | `curl.exe -i -X POST http://127.0.0.1:5000/join --data-urlencode "name=' OR '1'='1" -d "topic=Test" -d "service_id=1"`, then `SELECT id, group_name FROM tickets WHERE group_name LIKE '%OR%';` | `302 FOUND`, and one ticket whose name is exactly `' OR '1'='1`. No other rows were returned or changed. |

---

## Summary

| Layer | What it protects | Rules tested |
| --- | --- | --- |
| Browser | Honest users get fast feedback | 3 |
| Flask | The real gatekeeper: skipping the form still fails | 9 (plus the injection check) |
| Database | Integrity: no bug can save bad data | 15 |

*Check: every constraint type in `schema.md` has at least one row: FOREIGN KEY, NOT NULL, CHECK, UNIQUE, both partial unique indexes and ON DELETE RESTRICT.*