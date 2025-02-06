"use client";

import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/navigation";
import { saveUserToBackend, Auth0User } from "@/services/AuthService";

export default function LoginPage() {
    const { isAuthenticated, user, loginWithRedirect, getAccessTokenSilently } = useAuth0();
    const router = useRouter();

    useEffect(() => {
        if (isAuthenticated && user) {
            console.log("✅ User authenticated, saving to backend...");
            saveUserToBackend(user as Auth0User, getAccessTokenSilently).then(() => {
                console.log("✅ User saved, now redirecting...");
                router.push("/");
            }).catch(error => {
                console.error("❌ Error saving user before redirect:", error);
            });
        }
    }, [isAuthenticated, user, getAccessTokenSilently, router]);

    return (
        <div>
            <h1>Sign in to ThinkAI</h1>
            <div>
                <button onClick={() => loginWithRedirect({ authorizationParams: { prompt: "login" } })}>
                    Login/Signup
                </button>
            </div>
        </div>
    );
}
