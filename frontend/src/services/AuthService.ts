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
    if (!user) {
        console.log("❌ No user provided. Exiting saveUserToBackend.");
        return;
    }

    console.log("📡 Preparing to send request to backend. User Data:", user);

    const userMetadata = user["https://thinkai-api/user_metadata"] || {};

    try {
        const token = await getAccessTokenSilently();
        console.log("🔑 Got Auth0 Token:", token);

        const requestData = {
            auth0_id: user.sub,
            first_name: userMetadata.first_name || user.given_name || '',
            last_name: userMetadata.last_name || user.family_name || '',
            email: user.email,
        };

        console.log("📡 Sending request with data:", requestData);

        const response = await fetch('http://127.0.0.1:8000/api/users/save', {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(requestData),
        });

        console.log("📡 Response Status:", response.status);

        const data = await response.json();
        console.log("📡 Response Data:", data);

        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }

        console.log("✅ User saved successfully!");
    } catch (error) {
        console.error("❌ Error saving user:", error);
    }
}
