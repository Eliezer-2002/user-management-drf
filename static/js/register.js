(() => {
    "use strict";

    if (window.auth.hasSession()) {
        window.location.replace("/users/");
        return;
    }

    const form = document.getElementById("registerForm");
    const usernameInput = document.getElementById("username");
    const errorElements = {
        username: document.getElementById("username-error"),
        email: document.getElementById("email-error"),
        password: document.getElementById("password-error"),
    };

    usernameInput.addEventListener("input", () => {
        usernameInput.value = usernameInput.value.replace(/\s/g, "");
    });

    function renderErrors(errors) {
        Object.values(errorElements).forEach((element) => element.replaceChildren());
        Object.entries(errorElements).forEach(([field, element]) => {
            if (!errors[field]?.length) {
                return;
            }
            const message = document.createElement("p");
            message.className = "text-danger";
            message.textContent = errors[field][0];
            element.append(message);
        });
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const response = await fetch("/api/newuserregister/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    username: usernameInput.value,
                    email: document.getElementById("email").value,
                    password: document.getElementById("password1").value,
                    confirm_password: document.getElementById("password2").value,
                }),
            });
            const data = await response.json();
            if (!response.ok) {
                renderErrors(data);
                return;
            }
            window.location.assign("/");
        } catch (error) {
            window.appendAlert("Registration failed. Please try again.", "danger");
        }
    });
})();
