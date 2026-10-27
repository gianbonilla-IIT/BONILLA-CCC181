## Part 9: Accessibility check

**Goal:** make sure people using a keyboard, a screen reader, or a small screen can use every screen.

Do all three checks on **all three screens**, and record the results in `docs/week3/accessibility.md`.

**9a. Lighthouse.** In Chrome, open DevTools → **Lighthouse** → select **Accessibility** and **Mobile** → **Analyze page load**. Record the score for each screen. **Aim for 90 or higher.** Fix every issue it lists that you can, and run it again. Take a screenshot of each final score.

![Project Screenshot](screenshots\lighthouse-join.png)
![Project Screenshot](screenshots\lighthouse-queue.png)
![Project Screenshot](screenshots\lighthouse-staff.png)

**9b. Keyboard only.** Put your mouse away. Using only Tab, Shift+Tab, Enter, Space and the arrow keys:

- Join the queue from the home page.
- On the staff dashboard, filter by a service, call a ticket, and serve it.

Can you see where the focus is at every step? Can you reach and use every control? Does the skip link appear on the first Tab? Write down anything that failed and how you fixed it.

**9c. Manual checklist.** Check each item and mark it ✅ or ❌ (with the fix):

| Check | Join | My place | Staff |
| --- | --- | --- | --- |
| Every input has a visible label | | | |
| Error messages say what to do, in text | | | |
| Status is shown in words, not only color | | | |
| Text and buttons are readable at 375 px with no sideways page scroll | | | |
| Buttons are at least about 44 × 44 px on a phone | | | |
| Page has one `<h1>` and headings in order | | | |
| `<html lang="en">` (or your language) is set | | | |

**Checkpoint 9**

- [ ] `docs/week3/accessibility.md` has a Lighthouse score and screenshot for each screen, the keyboard test notes, and the completed checklist.
- [ ] Each screen scores 90 or higher, or the file explains what is left and why.
- [ ] Committed.

---