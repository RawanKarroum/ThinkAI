"use client"; 

import { Auth0Provider } from "@auth0/auth0-react";

const domain = process.env.NEXT_PUBLIC_AUTH0_DOMAIN!;
const clientId = process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID!;
const audience = process.env.NEXT_PUBLIC_AUTH0_AUDIENCE!;

export function AuthProvider({ children }: { children: React.ReactNode }) {
  if (!domain || !clientId || !audience) {
    console.error("🚨 Auth0 environment variables are missing! Check .env.local");
    return null; 
  }

  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        redirect_uri: typeof window !== "undefined" ? window.location.origin : "http://localhost:3000",
        audience: audience,
        scope: "openid profile email read:protected",
      }}
    >
      {children}
    </Auth0Provider>
  );
}
