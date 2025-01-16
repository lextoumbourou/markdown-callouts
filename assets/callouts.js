document.addEventListener("DOMContentLoaded", function () {
  // Initialize all collapsible callouts
  const collapsibleCallouts = document.querySelectorAll(".callout.is-collapsible");
  collapsibleCallouts.forEach(callout => {
    callout.classList.add("is-collapsed");
    const content = callout.querySelector(".callout-content");
    if (content) content.style.display = "none";
  });

  // Handle click events on callout titles
  document.addEventListener("click", function (event) {
    const header = event.target.closest(".callout-title");
    if (!header) return;

    const callout = header.closest(".callout.is-collapsible");
    if (!callout) return;

    callout.classList.toggle("is-collapsed");

    const content = callout.querySelector(".callout-content");
    if (!content) return;

    if (callout.classList.contains("is-collapsed")) {
      content.style.display = "none";
    } else {
      content.style.display = "";
    }
  });
}); 