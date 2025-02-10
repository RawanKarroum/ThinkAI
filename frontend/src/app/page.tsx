"use client"

import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/navigation";
import { Auth0User } from "@/services/AuthService";

export default function Home() {
  const { isAuthenticated, user }= useAuth0();
  const router = useRouter();
  const [firstName, setFirstName ] = useState<string | null>(null);

  useEffect(() => {
    if(!isAuthenticated){
      router.push("/login")
  } else if (user){
    const typedUser = user as Auth0User;
    const firstNameFromAuth0 = 
      typedUser["https://thinkai-api/user_metadata"]?.first_name ||
      typedUser.given_name ||
      typedUser.name?.split(" ")[0] || 
      "User";

      setFirstName(firstNameFromAuth0);
  }
}, [isAuthenticated, user, router]);

if(!isAuthenticated){
  return null;
}

  return (
    <>
    <h1>Welcome back, {firstName}</h1>
    </>
  );
}
