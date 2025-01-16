document.addEventListener("DOMContentLoaded", function () {
    // Initialize collapsed callouts
    const collapsedCallouts = document.querySelectorAll(".callout.is-collapsible.is-collapsed");
    collapsedCallouts.forEach(callout => {
        const content = callout.querySelector(".callout-content");
        if (content) content.style.display = "none";

        // Set initial chevron icon
        const foldIcon = callout.querySelector(".callout-fold");
        if (foldIcon) {
            foldIcon.setAttribute("data-lucide", "chevron-right");
            lucide.createIcons();
        }
    });

    // Handle click events on callout titles
    document.addEventListener("click", function (event) {
        const header = event.target.closest(".callout-title");
        if (!header) return;

        const callout = header.closest(".callout.is-collapsible");
        if (!callout) return;

        callout.classList.toggle("is-collapsed");

        const content = callout.querySelector(".callout-content");
        const foldIcon = callout.querySelector(".callout-fold");
        if (!content || !foldIcon) return;

        if (callout.classList.contains("is-collapsed")) {
            content.style.display = "none";
            foldIcon.setAttribute("data-lucide", "chevron-right");
        } else {
            content.style.display = "";
            foldIcon.setAttribute("data-lucide", "chevron-down");
        }

        // Refresh the Lucide icons
        lucide.createIcons();
    });
}); 