"use client";

import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useCallback, useState } from "react";

export default function AuthButtons() {
  const { loginWithRedirect, logout, isAuthenticated, user, getAccessTokenSilently } = useAuth0();
  const [apiMessage, setApiMessage] = useState<string | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  
  const saveUserToBackend = useCallback(async () => {
    if (!user) return;
  
    console.log("🔄 Checking user data before saving:", user);
    console.log("🔄 Extracting user_metadata:", user["https://thinkai-api/user_metadata"]);  
  
    const userMetadata = user["https://thinkai-api/user_metadata"] || {};
  
    try {
      const token = await getAccessTokenSilently();
  
      const requestData = {
        auth0_id: user.sub,
        first_name: userMetadata.first_name || '',
        last_name: userMetadata.last_name || '',
        email: user.email,
      };
  
      console.log("📡 Sending Request Data:", requestData);
  
      const response = await fetch('http://127.0.0.1:8000/api/users/save/', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(requestData),          
      });
  
      const responseData = await response.json();
      console.log("✅ API Response:", responseData);
  
    } catch (error) {
      console.error("❌ Error saving user:", error);
    }
  }, [user, getAccessTokenSilently]);
  
  
   
  
    useEffect(() => {
      if (isAuthenticated && user) {
        saveUserToBackend();
      }
    }, [isAuthenticated, user, saveUserToBackend]);
  const fetchAccessToken = async () => {
    try {
      const token = await getAccessTokenSilently();
      setAccessToken(token);
      console.log("✅ Auth0 Access Token:", token);
    } catch (error) {
      console.error("❌ Error getting token:", error);
      setAccessToken("Error retrieving token.");
    }
  };

  const callProtectedApi = async () => {
    if (!accessToken) {
      console.warn("⚠️ No access token found. Fetching token...");
      await fetchAccessToken();
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/users/protected/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP Error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("✅ API Response:", data);
      setApiMessage(data.message);
    } catch (error) {
      console.error("❌ Error accessing protected route:", error);
      setApiMessage("Error accessing API.");
    }
  };

  return (
    <div className="flex flex-col items-center space-y-4">
      {isAuthenticated ? (
        <>
          <p className="text-lg font-semibold">Welcome, {user?.name}</p>

          <button
            onClick={fetchAccessToken}
            className="px-4 py-2 bg-yellow-500 text-white rounded-lg"
          >
            Get Access Token
          </button>

          <button
            onClick={callProtectedApi}
            className="px-4 py-2 bg-green-500 text-white rounded-lg"
          >
            Call Protected API
          </button>

          <button
            onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
            className="px-4 py-2 bg-red-500 text-white rounded-lg"
          >
            Log Out
          </button>

          {accessToken && (
            <pre className="bg-gray-200 p-4 text-xs break-all">
              <strong>Access Token:</strong> {accessToken}
            </pre>
          )}

          {apiMessage && (
            <pre className="bg-gray-200 p-4">
              <strong>API Response:</strong> {apiMessage}
            </pre>
          )}
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