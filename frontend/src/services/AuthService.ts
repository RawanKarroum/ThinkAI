export interface Auth0User {
    sub: string;
    email: string;
    name?: string;
    given_name?: string;
    family_name?: string;
    "https://thinkai-api/user_metadata"?: {
        first_name?: string;
        last_name?: string;
    };  
}

//save auth0 user to backend
export async function saveUserToBackend(
    user: Auth0User | null,
    getAccessTokenSilently: () => Promise<string>
): Promise<void> {
    if(!user) return;

    const userMetadata = user["https://thinkai-api/user_metadata"] || {};

    try{
        const token = await getAccessTokenSilently();
        const requestData = {
            auth0_id: user.sub, 
            first_name: userMetadata.first_name || user.given_name || '',
            last_name: userMetadata.last_name || user.family_name || '',
            email: user.email, 
        };

        const response = await fetch('http://127.0.0.1:8000/api/users/save/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(requestData),
        });

        if(!response.ok){
            throw new Error("API request failed with status ${response.status}");
        }

        console.log("User saved to backend")
    } catch (error){
    console.error("Error saving user:", error);
    }
}