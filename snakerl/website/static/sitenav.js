/*
This JavaScript was written entirely by Claude Code.

Opens and closes the navigation sidebar (markup in base.html).

The sidebar slides in over the page (which is not dimmed). Each page starts with it in the
state the user last chose (open the first time).

The burger button toggles it. Clicking the page outside it or pressing
Escape closes it. It slides in and out when toggled, but not on page load.
*/

(function () {
    const toggle = document.getElementById("navToggle");
    const nav = document.getElementById("siteNav");
    const backdrop = document.getElementById("siteNavBackdrop");

    // Where the user's last open/closed choice is remembered (this browser only)
    const STORAGE_KEY = "siteNavOpen";

    function savedOpen() {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved === null ? null : saved === "true";
        } catch (e) {
            return null; // storage blocked (e.g. private window)
        }
    }

    function saveOpen(open) {
        try {
            localStorage.setItem(STORAGE_KEY, open);
        } catch (e) {
            // storage blocked: the sidebar still works, it just won't be remembered
        }
    }

    // Open or close because the user asked to, and remember that choice
    function choose(open) {
        setOpen(open);
        saveOpen(open);
    }

    function setOpen(open, moveFocus = true) {
        document.body.classList.toggle("site-nav-open", open);
        toggle.setAttribute("aria-expanded", open);
        toggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
        if (open && moveFocus) {
            // Move keyboard focus into the sidebar
            const first = nav.querySelector("a.site-nav-link");
            if (first) {
                first.focus({ preventScroll: true });
            }
        }
    }

    function isOpen() {
        return document.body.classList.contains("site-nav-open");
    }

    toggle.addEventListener("click", () => choose(!isOpen()));
    backdrop.addEventListener("click", () => choose(false));

    // Close after choosing a link (matters for links to a section on the same page)
    nav.addEventListener("click", (event) => {
        if (event.target.closest("a")) {
            setOpen(false);
        }
    });

    // Starting state: the user's last choice (open if they haven't chosen yet)
    setOpen(savedOpen() !== false, false);

    // Turn the slide animation on only after the starting state has rendered
    requestAnimationFrame(() => requestAnimationFrame(() => {
        document.body.classList.remove("site-nav-preload");
    }));

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && isOpen()) {
            choose(false);
            toggle.focus();
        }
    });
})();
