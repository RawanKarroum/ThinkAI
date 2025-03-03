"use client";

import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/navigation";
import { saveUserToBackend, Auth0User, fetchUserRole } from "@/services/AuthService";

export default function LoginPage() {
    const { isAuthenticated, user, loginWithRedirect, getAccessTokenSilently } = useAuth0();
    const router = useRouter();

    useEffect(() => {
        const handleLogin = async () => {
            if (isAuthenticated && user?.sub) {
                console.log("✅ User authenticated, saving to backend...");
                try{
                    await saveUserToBackend(user as Auth0User, getAccessTokenSilently);
    
                    console.log("✅ User saved, now redirecting...");
    
                    const role = await fetchUserRole(user.sub);
                    console.log("👤 User role:", role);
    
                    if(role === "teacher"){
                        router.push("/dashboards/teacher-dashboard");
                    } else if(role === "student"){
                        router.push("/dashboards/student-dashboard");
                    } else {
                        router.push("/");
                    }
                }   
                catch (error) {
                    console.error("❌ Error saving user before redirect:", error);
    
                }
            }
        }
        handleLogin();
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
