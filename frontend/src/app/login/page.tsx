"use client"

import { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
    const { isAuthenticated, loginWithRedirect } = useAuth0();
    const router = useRouter();

    useEffect(() => {
        if(isAuthenticated){
            router.push("/")
        }
    }, [isAuthenticated, router]);

    return (
        <div>
            <h1>Sign in to ThinkAI</h1>
            <div>
                <button onClick = {() => loginWithRedirect()}>Login/Signup</button>
            </div>
        </div>
    )
}