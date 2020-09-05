import React, { useEffect, useState } from 'react';
import Users from '../components/Users/Users';
import AddUserForm from '../components/Users/AddUserForm';
import axios from 'axios';
import Input from '../components/UI/Input/Input';


const UserContainer = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        if(users.length === 0) {
            axios.get("http://127.0.0.1:8080/api/v1/users").then(response => {
                setUsers(response.data);
                console.log(users);
            })
        }
    });

    const deleteUser = (id) => {
        axios.delete("http://127.0.0.1:8080/api/v1/users/"+id).then(response => {
            if (response.status === 200) {
                console.log("User successfully deleted") 
                axios.get("http://127.0.0.1:8080/api/v1/users").then(response => {
                    setUsers(response.data)
                }).catch(err => {
                    console.log(err)
                    alert(err)
                })
            } else {
                console.log(response)
            }
        }).catch(err => {
            alert(err.response.data.message)
        });
    }
    return (
        <div>
            <AddUserForm users={users} setUser={setUsers}/>
            <Users users={users} delFunc={deleteUser}/>
        </div>
    )
}

export default UserContainer;