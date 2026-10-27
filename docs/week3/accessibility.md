## Part 9: Accessibility check

**Goal:** make sure people using a keyboard, a screen reader, or a small screen can use every screen.

Do all three checks on **all three screens**, and record the results in `docs/week3/accessibility.md`.

**9a. Lighthouse.** In Chrome, open DevTools → **Lighthouse** → select **Accessibility** and **Mobile** → **Analyze page load**. Record the score for each screen. **Aim for 90 or higher.** Fix every issue it lists that you can, and run it again. Take a screenshot of each final score.

![join page: 100/100](screenshots\lighthouse-join.png)
![queue page: 96/100](screenshots\lighthouse-queue.png)
![staff page: 96/100](screenshots\lighthouse-staff.png)

**9b. Keyboard only.** Put your mouse away. Using only Tab, Shift+Tab, Enter, Space and the arrow keys:

- Join the queue from the home page.
- On the staff dashboard, filter by a service, call a ticket, and serve it.

![successfully joined the queue, keyboard only](screenshots\nomouse-test1.png)
![successfully navigated around staff dashboard, keyboard only](screenshots\nomouse-test2.png)

Can you see where the focus is at every step? **Yes**

Can you reach and use every control? **Yes**

Does the skip link appear on the first Tab? **Yes**

Write down anything that failed and how you fixed it:

The "Call Next" button in the staff page didn't have a focus-shadow when selected upon going into this section. I didn't notice it at first by using a mouse, but when I navigated using a keyboard, I immediately noticed it. I first thought it wasn't being selected in the first place. Upon observing it close, there was a faint change in the background color when selected, so I diagnosed it as a lack in the css.

**9c. Manual checklist.** Check each item and mark it ✅ or ❌ (with the fix):

| Check | Join | My place | Staff |
| --- | --- | --- | --- |
| Every input has a visible label | ✅ | ✅ | ✅ |
| Error messages say what to do, in text | ✅ | ✅ | ✅ |
| Status is shown in words, not only color | ✅ | ✅ | ✅ |
| Text and buttons are readable at 375 px with no sideways page scroll | ✅ | ✅ | ✅ |
| Buttons are at least about 44 × 44 px on a phone | ✅	 | ✅ | ❌ (action buttons were 31x32, now fixed by setting a min of 44x44)|
| Page has one `<h1>` and headings in order | ✅ | ❌ (there is no need for a dedicated h1, for there is already a span element using bootstrap's display-1 css class) | ✅ |
| `<html lang="en">` (or your language) is set | ✅ | ✅ | ✅ |

**Checkpoint 9**

- [x] `docs/week3/accessibility.md` has a Lighthouse score and screenshot for each screen, the keyboard test notes, and the completed checklist.
- [x] Each screen scores 90 or higher, or the file explains what is left and why.
- [x] Committed.

---