/* Show a dismissible error banner */

function showError(text) {
    // don't stack the same message if the button is clicked repeatedly
    const existing = Array.from(document.querySelectorAll(".alert"));
    if (existing.some((alert) => alert.dataset.message === text)) {
        return;
    }

    // create error banner
    const alert = document.createElement("div");
    alert.className = "alert alert-danger alert-dismissible";
    alert.setAttribute("role", "alert");
    alert.dataset.message = text;
    alert.textContent = text;

    // add button to close error banner
    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "close";
    closeBtn.setAttribute("aria-label", "Close");
    closeBtn.innerHTML = '<span aria-hidden="true">&times;</span>';
    closeBtn.addEventListener("click", () => alert.remove());
    alert.appendChild(closeBtn);

    document.getElementById("flash-messages").appendChild(alert);
}
