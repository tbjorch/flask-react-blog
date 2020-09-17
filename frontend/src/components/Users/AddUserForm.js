import React, { useState } from 'react';
import Card from '../UI/Card/Card';
import Button from '../UI/Button/Button';
import Input from '../UI/Input/Input';
import classes from './Users.module.css';
import axios from 'axios';
import Select from '../UI/Select/Select';

const AddUserForm = (props) => {
    const [user, setUser] = useState({'username':"", 'password':""});
    const [role, setRole] = useState("");

    const usernameChangeHandler = (event) => {
        const newUser = {...user};
        newUser.username = event.target.value;
        setUser(newUser);
    }

    const passwordChangeHandler = (event) => {
        const newUser = {...user};
        newUser.password = event.target.value;
        setUser(newUser);
    }

    const roleChangeHandler = (event) => {
        setRole(event.target.value);
    }

    const addUser = (user) => {
        axios.post("http://127.0.0.1:8080/api/v1/users", user, {
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            console.log(response.data.message);
            user.username = "";
            user.password = "";
            axios.get("http://127.0.0.1:8080/api/v1/users").then(response => {
                props.setUser(response.data);
            }).catch(err => {
                console.log(err)
            })
        }).catch(err => {
            console.log(err)
            alert(err)
        })
    };

    const roles = [{value: "admin"}, {value: "user"}];

    const content = (
        <div>
            <form>
                <h1>Add User</h1>
                <Input label="Username" placeholder="Username" type="text" value={user.username} onChange={usernameChangeHandler}/>
                <Input label="Password" placeholder="Password" type="password" value={user.password} onChange={passwordChangeHandler}/>
                <Select label="Role" options={roles} value={role} onChange={roleChangeHandler}/>
            </form>
            <Button title={"ADD USER"} onClick={() => addUser(user)}/>
        </div>
    )
    return (
        <Card content={content}/>
    );
}

export default AddUserForm;