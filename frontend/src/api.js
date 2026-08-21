const BASE_URL = "http://localhost:8000";

async function request(path, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    const res = await fetch(`${BASE_URL}${path}`, {
        ...options,
        headers,
        credentials: "include",
    });

    if (!res.ok) {
        let detail = `Request failed (${res.status})`;

        try {
            const body = await res.json();
            detail = body.detail || body.message || detail;
        } catch {
            // Ignore non-JSON error responses
        }

        throw new Error(detail);
    }

    if (res.status === 204) {
        return null;
    }

    return res.json();
}


// Authentication

export function login(email) {
    return request("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email }),
    });
}

export function verifyCode(email, code) {
    return request("/auth/verify", {
        method: "POST",
        body: JSON.stringify({
            email,
            code,
        }),
    });
}


// Users

export function createUser(payload) {
    return request("/users/", {
        method: "POST",
        body: JSON.stringify(payload),
    });
}

export function getCurrentUser() {
    return request("/users/me", {
        method: "GET",
    });
}

export function updateUser(payload) {
    return request("/users/me", {
        method: "PUT",
        body: JSON.stringify(payload),
    });
}

export function deleteUser() {
    return request("/users/me", {
        method: "DELETE",
    });
}


// Recommendations

export function generateAndSendRecommendation() {
    return request("/recommendations/me", {
        method: "POST",
    });
}

export function getRecommendations() {
    return request("/recommendations/me", {
        method: "GET",
    });
}

export function logout() {
    return request("/auth/logout", {
        method: "POST",
    });
}