(() => {
    "use strict";

    if (window.auth.hasSession()) {
        window.location.replace("/users/");
        return;
    }

    const form = document.getElementById("loginForm");
    const submitButton = document.getElementById("loginButton");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        submitButton.disabled = true;

        try {
            const response = await fetch("/api/token/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    username: document.getElementById("username").value,
                    password: document.getElementById("password").value,
                }),
            });

            if (!response.ok) {
                throw new Error("Username or password is incorrect.");
            }

            const data = await response.json();
            window.auth.storeTokens(data.access, data.refresh);
            window.location.assign("/users/");
        } catch (error) {
            window.appendAlert(error.message || "Login failed.", "danger");
        } finally {
            submitButton.disabled = false;
        }
    });
})();
