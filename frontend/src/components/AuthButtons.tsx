"use client";

import { useAuth0 } from "@auth0/auth0-react";
import { useState } from "react";

export default function AuthButtons() {
  const { loginWithRedirect, logout, isAuthenticated, user, getAccessTokenSilently } = useAuth0();
  const [apiMessage, setApiMessage] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  // ✅ Function to get the token and log it
  const fetchAccessToken = async () => {
    try {
      const token = await getAccessTokenSilently(); 
      setAccessToken(token);
      console.log("Auth0 Access Token:", token);
    } catch (error) {
      console.error("Error getting token:", error);
      setAccessToken("Error retrieving token.");
    }
  }

  // ✅ Function to call the protected API
  const callProtectedApi = async () => {
    try {
      const token = await getAccessTokenSilently();
  
      const response = await fetch("http://127.0.0.1:8000/api/users/protected/", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,  // ✅ Ensure token is here
          "Content-Type": "application/json",
        },
      });
  
      const data = await response.json();
      console.log("✅ API Response:", data);
    } catch (error) {
      console.error("❌ Error accessing protected route:", error);
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {isAuthenticated ? (
        <>
          <p className="text-lg font-semibold">Welcome, {user?.name}</p>
          
          {/* ✅ Get Access Token Button */}
          <button onClick={fetchAccessToken} className="px-4 py-2 bg-yellow-500 text-white rounded-lg">
            Get Access Token
          </button>

          {/* ✅ Call Protected API Button */}
          <button onClick={callProtectedApi} className="px-4 py-2 bg-green-500 text-white rounded-lg">
            Call Protected API
          </button>

          {/* ✅ Logout Button */}
          <button
            onClick={() => logout()}
            className="px-4 py-2 bg-red-500 text-white rounded-lg"
          >
            Log Out
          </button>

          {/* ✅ Display the access token */}
          {accessToken && (
            <pre className="bg-gray-200 p-4 text-xs break-all">
              <strong>Access Token:</strong> {accessToken}
            </pre>
          )}

          {/* ✅ Display API response */}
          {apiMessage && <pre className="bg-gray-200 p-4">{apiMessage}</pre>}
        </>
      ) : (
        <button
          onClick={() => loginWithRedirect()}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg"
        >
          Log In
        </button>
      )}
    </div>
  );
}
