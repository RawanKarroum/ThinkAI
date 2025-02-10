"use client"

import { useAuth0 } from "@auth0/auth0-react"
import { saveUserToBackend, Auth0User } from "@/services/AuthService"
import { useEffect, useState } from "react"
import React from "react"

export default function AuthButtons() {
  const { loginWithRedirect, logout, user, getAccessTokenSilently, isAuthenticated } = useAuth0()
  const [firstName, setFirstName] = useState<string | null>(null);

  //save user to backend on authentication and extract first name
  useEffect(() => {
    if( isAuthenticated && user){
      const typedUser = user as Auth0User;
      saveUserToBackend(typedUser, getAccessTokenSilently)

      const firstNameFromAuth0 = 
        typedUser["https://thinkai-api/user_metadata"]?.first_name || 
        typedUser.given_name || 
        typedUser.name?.split(" ")[0] || "User";
        
        setFirstName(firstNameFromAuth0)
    }
  }, [isAuthenticated, user, getAccessTokenSilently])

  return (
    <div>
      {isAuthenticated ? (
        <>
          <p>Hi, {firstName}</p>

          <button onClick = {() => logout({logoutParams : {returnTo: window.location.origin }})}> 
             Logout
          </button>
        </>
      ) : (
        <button onClick = {() => loginWithRedirect()}>
          Login
        </button>
      )}
  </div>
  );
}