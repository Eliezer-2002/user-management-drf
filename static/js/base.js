(() => {
    "use strict";

    const alertPlaceholder = document.getElementById("liveAlertPlaceholder");
    const allowedTypes = new Set(["danger", "info", "success", "warning"]);

    window.appendAlert = (message, type = "info") => {
        const alertType = allowedTypes.has(type) ? type : "info";
        const alert = document.createElement("div");
        alert.className = `alert alert-${alertType} alert-dismissible mt-4`;
        alert.setAttribute("role", "alert");

        const content = document.createElement("div");
        content.textContent = String(message);

        const closeButton = document.createElement("button");
        closeButton.type = "button";
        closeButton.className = "btn-close";
        closeButton.dataset.bsDismiss = "alert";
        closeButton.setAttribute("aria-label", "Close");

        alert.append(content, closeButton);
        alertPlaceholder.append(alert);
    };
})();
