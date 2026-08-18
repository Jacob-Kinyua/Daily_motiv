const BASE_URL = "http://localhost:8000";

async function request(path, options = {}) {
    const res = await fetch(`${BASE_URL}${path}`, {
        headers: {
            "Content-Type": "application/json",
        },
        ...options,
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


// Users

export function createUser(payload) {
    return request("/users/", {
        method: "POST",
        body: JSON.stringify(payload),
    });
}

export function deleteUser(userId) {
    return request(`/users/${userId}`, {
        method: "DELETE",
    });
}


// Recommendations

export function generateAndSendRecommendation(userId) {
    return request(`/recommendations/${userId}`, {
        method: "POST",
    });
}

export function getRecommendations(userId) {
    return request(`/recommendations/${userId}`);
}