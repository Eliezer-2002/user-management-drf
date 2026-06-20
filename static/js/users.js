(() => {
    "use strict";

    const elements = {
        cancelDelete: document.getElementById("cancelDeleteButton"),
        cancelLogout: document.getElementById("cancelLogoutButton"),
        confirmDelete: document.getElementById("confirmDeleteButton"),
        confirmLogout: document.getElementById("confirmLogoutButton"),
        createAlert: document.getElementById("CreateUserFormAlert"),
        createForm: document.getElementById("createUserForm"),
        nextPage: document.getElementById("nextPageButton"),
        pageButtons: document.getElementById("pageBtns"),
        previousPage: document.getElementById("prevPageButton"),
        search: document.getElementById("search"),
        searchForm: document.getElementById("searchForm"),
        updateAlert: document.getElementById("UpdateUserFormAlert"),
        updateForm: document.getElementById("updateUserForm"),
        userId: document.getElementById("userId"),
        userList: document.getElementById("userList"),
    };

    let nextUrl = null;
    let previousUrl = null;
    let listRequestController = null;

    function hideModal(id) {
        const modal = bootstrap.Modal.getOrCreateInstance(document.getElementById(id));
        modal.hide();
    }

    function renderFormAlert(container, message, type = "danger") {
        const text = document.createElement("p");
        text.className = `text-${type}`;
        text.textContent = message;
        container.replaceChildren(text);
    }

    function firstError(errors, fallback) {
        for (const value of Object.values(errors || {})) {
            if (Array.isArray(value) && value.length) {
                return value[0];
            }
        }
        return fallback;
    }

    function redirectToLogin() {
        window.auth.clearSession();
        window.location.replace("/");
    }

    async function parseJson(response) {
        const contentType = response.headers.get("content-type") || "";
        return contentType.includes("application/json") ? response.json() : {};
    }

    function makeIconButton({className, iconName, label, modalId, onClick}) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = className;
        button.dataset.bsToggle = "modal";
        button.dataset.bsTarget = `#${modalId}`;
        button.setAttribute("aria-label", label);
        button.title = label;
        button.addEventListener("click", onClick);

        const icon = document.createElement("ion-icon");
        icon.className = "fs-5";
        icon.setAttribute("name", iconName);
        button.append(icon);
        return button;
    }

    function createUserCard(user) {
        const column = document.createElement("div");
        column.className = "user-col col-md-6 col-lg-4 col-xxl-3 mb-3 mb-sm-0";

        const card = document.createElement("div");
        card.className = "user-card card";
        const body = document.createElement("div");
        body.className = "card-body d-flex p-3 align-items-center";
        const info = document.createElement("div");
        info.className = "me-auto card-info";
        const username = document.createElement("h5");
        username.className = "card-title";
        username.textContent = user.username;
        const email = document.createElement("p");
        email.className = "card-text";
        email.textContent = user.email;
        info.append(username, email);

        const buttons = document.createElement("div");
        buttons.className = "user-btns d-flex flex-column ms-auto";
        buttons.append(
            makeIconButton({
                className: "btn btn-warning mb-1",
                iconName: "create-outline",
                label: `Edit ${user.username}`,
                modalId: "UserUpdateModal",
                onClick: () => populateUpdateForm(user.id),
            }),
            makeIconButton({
                className: "btn btn-danger mt-1",
                iconName: "trash-outline",
                label: `Delete ${user.username}`,
                modalId: "DeleteUserBackdrop",
                onClick: () => {
                    elements.userId.value = user.id;
                },
            }),
        );
        body.append(info, buttons);
        card.append(body);
        column.append(card);
        return column;
    }

    async function loadUsers(url = null) {
        listRequestController?.abort();
        listRequestController = new AbortController();

        const params = new URLSearchParams({page: "1"});
        if (elements.search.value.trim()) {
            params.set("search", elements.search.value.trim());
        }
        const finalUrl = url || `/api/users/?${params}`;

        try {
            const response = await window.auth.fetchWithAuth(finalUrl, {
                signal: listRequestController.signal,
            });
            if (response.status === 401 || response.status === 403) {
                redirectToLogin();
                return;
            }
            if (!response.ok) {
                throw new Error("Unable to load users.");
            }

            const data = await response.json();
            elements.userList.replaceChildren(...data.results.map(createUserCard));
            nextUrl = data.next;
            previousUrl = data.previous;
            elements.nextPage.disabled = !nextUrl;
            elements.previousPage.disabled = !previousUrl;
            elements.pageButtons.hidden = !nextUrl && !previousUrl;
        } catch (error) {
            if (error.name !== "AbortError") {
                if (!window.auth.hasSession()) {
                    redirectToLogin();
                    return;
                }
                window.appendAlert(error.message || "Unable to load users.", "warning");
            }
        }
    }

    async function populateUpdateForm(userId) {
        elements.userId.value = userId;
        elements.updateAlert.replaceChildren();

        try {
            const response = await window.auth.fetchWithAuth(`/api/users/${userId}/retrieve/`);
            if (!response.ok) {
                throw new Error("User not found.");
            }
            const data = await response.json();
            document.getElementById("updateUsername").value = data.username;
            document.getElementById("updateEmail").value = data.email;
        } catch (error) {
            hideModal("UserUpdateModal");
            window.appendAlert(error.message || "User not found.", "warning");
            await loadUsers();
        }
    }

    elements.searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        loadUsers();
    });
    elements.previousPage.addEventListener("click", () => previousUrl && loadUsers(previousUrl));
    elements.nextPage.addEventListener("click", () => nextUrl && loadUsers(nextUrl));

    [document.getElementById("newUsername"), document.getElementById("updateUsername")].forEach(
        (input) => input.addEventListener("input", () => {
            input.value = input.value.replace(/\s/g, "");
        }),
    );

    elements.createForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = {
            username: document.getElementById("newUsername").value.trim(),
            email: document.getElementById("newEmail").value.trim(),
            password: document.getElementById("newPassword").value,
        };

        try {
            const response = await window.auth.fetchWithAuth("/api/users/create/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            const data = await parseJson(response);
            if (!response.ok) {
                renderFormAlert(
                    elements.createAlert,
                    firstError(data, "User creation failed."),
                );
                return;
            }
            elements.createForm.reset();
            elements.createAlert.replaceChildren();
            hideModal("UserCreateModal");
            await loadUsers();
            window.appendAlert("User created successfully.", "success");
        } catch (error) {
            renderFormAlert(elements.createAlert, error.message || "User creation failed.");
        }
    });

    elements.updateForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const userId = elements.userId.value;
        const payload = {
            username: document.getElementById("updateUsername").value.trim(),
            email: document.getElementById("updateEmail").value.trim(),
        };

        try {
            const response = await window.auth.fetchWithAuth(`/api/users/${userId}/update/`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload),
            });
            const data = await parseJson(response);
            if (!response.ok) {
                renderFormAlert(
                    elements.updateAlert,
                    firstError(data, "User update failed."),
                );
                return;
            }
            elements.updateAlert.replaceChildren();
            hideModal("UserUpdateModal");
            await loadUsers();
            window.appendAlert("User updated successfully.", "success");
        } catch (error) {
            renderFormAlert(elements.updateAlert, error.message || "User update failed.");
        }
    });

    elements.cancelDelete.addEventListener("click", () => hideModal("DeleteUserBackdrop"));
    elements.confirmDelete.addEventListener("click", async () => {
        try {
            const response = await window.auth.fetchWithAuth(
                `/api/users/${elements.userId.value}/delete/`,
                {method: "DELETE"},
            );
            if (!response.ok) {
                throw new Error("Deletion failed.");
            }
            hideModal("DeleteUserBackdrop");
            await loadUsers();
            window.appendAlert("User deleted successfully.", "success");
        } catch (error) {
            window.appendAlert(error.message || "Deletion failed.", "warning");
        }
    });

    elements.cancelLogout.addEventListener("click", () => hideModal("LogoutBackdrop"));
    elements.confirmLogout.addEventListener("click", () => {
        window.auth.clearSession();
        window.location.assign("/");
    });

    document.querySelectorAll(".modal").forEach((modal) => {
        modal.addEventListener("hide.bs.modal", () => {
            if (document.activeElement instanceof HTMLElement) {
                document.activeElement.blur();
            }
        });
    });

    loadUsers();
})();
