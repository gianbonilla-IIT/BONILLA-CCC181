# Peristence Test

I followed the restart test as instructed in hw4.

## Restart Test

1. Create at least **five tickets** across at least two services. Call one, serve one, and let one person leave.

2. 📷 The staff dashboard, and the result of `SELECT id, status, service_id, created_at FROM tickets ORDER BY id;` in psql.
![Dashboard before restart](screenshots\11a-screenshot_1.png)

3. Stop Flask with Ctrl+C. Run `docker compose down`. Run `docker compose ps` and see that nothing is running.

4. Run `docker compose up -d`, wait until `docker compose ps` says **healthy**, then start Flask again.

5. 📷 The same dashboard and the same SQL query. Every ticket, status and time must be exactly as before.
![Dashboard after restart](screenshots\11a-screenshot_2.png)

## Rebuild from Scratch


>Your migrations should be able to rebuild the whole database on any computer, including your instructor's. Test it. **This deletes all your data**, so do it only after 11a:
>```
>docker compose down -v
>docker compose up -d
>flask --app app db upgrade
>flask --app app seed
>```
>The app must open, show your services on the join form, and let you join. If it fails, a table or column is missing from your migrations (or you used `db.create_all()` somewhere). Fix it with a **new** migration and try again. Write the result in `persistence.md`.

#### RESULT:

![Before migration](screenshots\11b-screenshot_1.png)

![After migration](screenshots\11b-screenshot_2.png)

Results are expected. As shown in the psql in powershell, these were the only seeded records in the migrations, and they were passed successfully to the front-end.