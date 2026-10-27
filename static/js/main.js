// ClassQ: shared behaviors

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