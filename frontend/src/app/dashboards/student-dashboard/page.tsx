"use client"

import {useAuth0} from "@auth0/auth0-react";  

const TeachersDashboard: React.FC = () => {
    const { user } = useAuth0();

    return(
        <div>
            <p>Welcomre student {user?.name}</p>
        </div>
    )
}

export default TeachersDashboard;