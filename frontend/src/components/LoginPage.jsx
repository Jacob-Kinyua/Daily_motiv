import { useState } from "react";
import { login, verifyCode } from "../api.js";

export default function LoginPage({ onLogin, onSignup }) {
    const [email, setEmail] = useState("");
    const [code, setCode] = useState("");

    const [codeSent, setCodeSent] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    async function handleLoginRequest(e) {
        e.preventDefault();

        setError("");
        setMessage("");
        setLoading(true);

        try {
            await login(email);

            setCodeSent(true);
            setMessage("Verification code sent.");
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleVerifyCode(e) {
        e.preventDefault();

        setError("");
        setMessage("");
        setLoading(true);

        try {
            // The backend sets the HttpOnly access_token cookie.
            await verifyCode(email, code);

            if (onLogin) {
                onLogin();
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-page">
            <h1>Log in</h1>

            {!codeSent ? (
                <form onSubmit={handleLoginRequest}>
                    <label htmlFor="email">
                        Email
                    </label>

                    <input
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        required
                    />

                    <button type="submit" disabled={loading}>
                        {loading
                            ? "Sending..."
                            : "Send verification code"}
                    </button>
                </form>
            ) : (
                <form onSubmit={handleVerifyCode}>
                    <p>
                        Enter the verification code sent to{" "}
                        <strong>{email}</strong>
                    </p>

                    <label htmlFor="code">
                        Verification code
                    </label>

                    <input
                        id="code"
                        type="text"
                        value={code}
                        onChange={(e) => setCode(e.target.value)}
                        placeholder="Enter 6-digit code"
                        maxLength={6}
                        required
                    />

                    <button type="submit" disabled={loading}>
                        {loading ? "Verifying..." : "Verify code"}
                    </button>

                    <button
                        type="button"
                        onClick={() => {
                            setCodeSent(false);
                            setCode("");
                            setError("");
                            setMessage("");
                        }}
                    >
                        Use a different email
                    </button>
                </form>
            )}

            {message && <p>{message}</p>}

            {error && <p>{error}</p>}

            <div className="signup-option">
                <p>Don't have an account?</p>

                <button
                    type="button"
                    onClick={onSignup}
                >
                    Sign up
                </button>
            </div>
        </div>
    );
}