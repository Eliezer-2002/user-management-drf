(() => {
    "use strict";

    const ACCESS_KEY = "token";
    const REFRESH_KEY = "refresh";
    let refreshRequest = null;

    function clearSession() {
        localStorage.removeItem(ACCESS_KEY);
        localStorage.removeItem(REFRESH_KEY);
    }

    function hasSession() {
        return Boolean(localStorage.getItem(ACCESS_KEY) && localStorage.getItem(REFRESH_KEY));
    }

    async function requestAccessToken() {
        const refresh = localStorage.getItem(REFRESH_KEY);
        if (!refresh) {
            throw new Error("No refresh token is available.");
        }

        const response = await fetch("/api/token/refresh/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({refresh}),
        });

        if (!response.ok) {
            clearSession();
            throw new Error("Your session has expired.");
        }

        const data = await response.json();
        localStorage.setItem(ACCESS_KEY, data.access);
        return data.access;
    }

    function refreshAccessToken() {
        if (!refreshRequest) {
            refreshRequest = requestAccessToken().finally(() => {
                refreshRequest = null;
            });
        }
        return refreshRequest;
    }

    async function fetchWithAuth(url, options = {}, canRetry = true) {
        let access = localStorage.getItem(ACCESS_KEY);
        if (!access && localStorage.getItem(REFRESH_KEY)) {
            access = await refreshAccessToken();
        }

        const headers = new Headers(options.headers || {});
        if (access) {
            headers.set("Authorization", `Bearer ${access}`);
        }

        const response = await fetch(url, {...options, headers});
        if (response.status === 401 && canRetry && localStorage.getItem(REFRESH_KEY)) {
            await refreshAccessToken();
            return fetchWithAuth(url, options, false);
        }
        return response;
    }

    window.auth = {
        clearSession,
        fetchWithAuth,
        hasSession,
        storeTokens(access, refresh) {
            localStorage.setItem(ACCESS_KEY, access);
            localStorage.setItem(REFRESH_KEY, refresh);
        },
    };
})();
