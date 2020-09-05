import React, { useState } from 'react';
import Backdrop from '../UI/Backdrop/Backdrop';
import Modal from '../UI/Modal/Modal';
import Button from '../UI/Button/Button';
import axios from 'axios';

const RegisterForm = (props) => {
    const [credentials, setCredentials] = useState({'username':"", 'password':""});

    const usernameChangeHandler = (event) => {
        const newCredentials = {...credentials};
        newCredentials.username = event.target.value;
        setCredentials(newCredentials);
    }

    const passwordChangeHandler = (event) => {
        const newCredentials = {...credentials};
        newCredentials.password = event.target.value;
        setCredentials(newCredentials);
    }

    const registerHandler = (credentials) => {
        axios.post("http://127.0.0.1:8080/api/v1/users", credentials, {
        headers: {
            "Content-Type": "application/json"
        }
        }).then(response => {
        console.log(response.data.message);
        props.show(false);
        props.redirect("/");
        })
    }

    const form = (
        <div style={{padding: "2em 0 4em 0"}}>
            <form>
                <h1>Register</h1>
                <input value={credentials.username} onChange={event => usernameChangeHandler(event)} placeholder="username" type="text"/>
                <input type="password" value={credentials.password} onChange={event => passwordChangeHandler(event)} placeholder="password"/>
            </form>
            <Button onClick={() => registerHandler(credentials)
            } title="REGISTER" />
        </div >
    )

    return (
        <div>
            <Backdrop show={true} clicked={props.show}/>
            <Modal element={form}/>
        </div>
    );
}

export default RegisterForm;