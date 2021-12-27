import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

const Profile = () => {
    const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
    
    if (isAuthenticated) {
        getAccessTokenSilently().then(accessToken => {
            console.log(accessToken)
            accessToken = accessToken
        });
    }
    

    return (
        <div>
            {JSON.stringify(user, null, 2)}
        </div>
    )
}

export default Profile;