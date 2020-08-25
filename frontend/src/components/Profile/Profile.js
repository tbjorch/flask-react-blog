import React from 'react';


const Profile = () => {
    return (
        <div>
            <form>
                <h1>Profile</h1>
                <input placeholder="Username" type="text"/>
                <input placeholder="Roles" type="text"/>
                <input placeholder="Member since" type="text" readOnly/>
                <input placeholder="Last updated" type="text" readOnly/>
            </form>
        </div>
    )
}

export default Profile;