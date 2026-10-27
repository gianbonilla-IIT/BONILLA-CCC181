// Confirm before submitting any form that has a data-confirm message.
document.addEventListener("submit", (event) => {
  const form = event.target.closest("form[data-confirm]");
  if (form && !window.confirm(form.dataset.confirm)) {
    event.preventDefault();
  }
});

// 1. Clear a field's error as soon as the user edits it.
//    Bootstrap only shows .invalid-feedback next to an .is-invalid field,
//    so removing the class hides the message too.
document.querySelectorAll("#join-form input, #join-form select").forEach((field) => {
  const clear = () => {
    field.classList.remove("is-invalid");
    field.removeAttribute("aria-describedby");
  };
  field.addEventListener("input", clear);
  field.addEventListener("change", clear); // selects fire "change"
});

// 2. Auto-dismiss alerts. Errors stay longer than success messages.
document.querySelectorAll(".alert").forEach((alertEl) => {
  const delay = alertEl.classList.contains("alert-danger") ? 3000 : 2000;
  let timer = setTimeout(close, delay);

  function close() {
    bootstrap.Alert.getOrCreateInstance(alertEl).close();
  }

  // Don't dismiss while the user is hovering or focusing it.
  alertEl.addEventListener("mouseenter", () => clearTimeout(timer));
  alertEl.addEventListener("mouseleave", () => { timer = setTimeout(close, 1000); });
  alertEl.addEventListener("focusin", () => clearTimeout(timer));
});

// 8a. Stop double joining: disable the button once the join form is submitted.
const joinForm = document.getElementById("join-form");
if (joinForm) {
  joinForm.addEventListener("submit", () => {
    const button = joinForm.querySelector("button[type=submit]");
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });
  // Coming back with the Back button can restore the page with the button still disabled.
  window.addEventListener("pageshow", (e) => {
    if (e.persisted) {
      const button = joinForm.querySelector("button[type=submit]");
      button.disabled = false;
      button.textContent = "Enter Queue";
    }
  });
}

// 8b. Keep My place up to date without reloading.
const liveRegion = document.getElementById("live-region");
if (liveRegion) {
  const statusUrl = liveRegion.dataset.statusUrl;
  const joinUrl = liveRegion.dataset.joinUrl;
  let timer;

  function render(data) {
    // Status badge (the color and dot come from the status-* class)
    const badge = document.getElementById("status-badge");
    badge.className = `badge status-badge status-${data.status}`;
    badge.textContent = data.status.replace("-", " ");

    // Position sentence
    const n = data.ahead.length;
    let sentence = "";
    if (data.status === "called") sentence = "It's your turn!";
    else if (data.status === "waiting") {
      sentence = n === 0 ? "You're next!" : `${n} ${n === 1 ? "person" : "people"} ahead of you`;
    }
    document.getElementById("position-text").textContent = sentence;

    // Currently entertaining + upcoming pills
    document.getElementById("current-number").textContent = data.current || "—";
    document.getElementById("upcoming-count").textContent = n;
    const box = document.getElementById("upcoming");
    box.replaceChildren();
    if (n === 0) {
      const empty = document.createElement("span");
      empty.className = "text-body-secondary";
      empty.textContent = "No one ahead of you";
      box.appendChild(empty);
    } else {
      data.ahead.slice(0, 4).forEach((label, i) => {
        const pill = document.createElement("span");
        pill.className = "badge rounded-pill text-bg-light border fs-6" + (i === 3 ? " d-none d-md-inline" : "");
        pill.textContent = label;
        box.appendChild(pill);
      });
    }

    // Buttons that only apply to some statuses
    document.getElementById("join-call").hidden = data.status !== "called";
    document.getElementById("leave-form").hidden = !["waiting", "called"].includes(data.status);

    // Nothing more can change once the ticket is finished
    if (["served", "no-show"].includes(data.status)) clearInterval(timer);
  }

  async function refreshStatus() {
    try {
      const res = await fetch(statusUrl);
      if (res.status === 404) {          // ticket was deleted (for example by staff)
        window.location.href = joinUrl;
        return;
      }
      if (!res.ok) return;
      render(await res.json());
    } catch (err) {
      console.warn("Could not refresh status", err);
    }
  }

  timer = setInterval(refreshStatus, 10000);
  // Refresh right away when the student comes back to the tab.
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) refreshStatus();
  });
}

// Staff dashboard: keep the queue up to date without reloading.
if (document.getElementById("queue-body")) {
  const regionIds = ["queue-count", "queue-body", "call-area"];

  async function refreshStaff() {
    const current = regionIds.map((id) => document.getElementById(id));

    // Don't swap content under the teacher's cursor or keyboard focus.
    const busy = current.some(
      (el) => el.contains(document.activeElement) || el.querySelector("button:hover")
    );
    if (busy) return;

    try {
      const res = await fetch(window.location.href, { headers: { "X-Live": "1" } });
      if (!res.ok) return;
      const doc = new DOMParser().parseFromString(await res.text(), "text/html");

      regionIds.forEach((id) => {
        const fresh = doc.getElementById(id);
        const old = document.getElementById(id);
        // Only touch the page when something actually changed.
        if (fresh && old && fresh.innerHTML !== old.innerHTML) {
          old.innerHTML = fresh.innerHTML;
        }
      });
    } catch (err) {
      console.warn("Could not refresh the dashboard", err);
    }
  }

  setInterval(refreshStaff, 5000);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) refreshStaff();
  });
}
