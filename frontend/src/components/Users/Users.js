import React, { useState } from 'react';
import Card from '../UI/Card/Card';
import Button from '../UI/Button/Button'
import classes from './Users.module.css';

const Users = (props) => {
    const table= props.users.map((user) => {
        const list = (
            <tr key={user.id} className={classes.tr}>
                <td className={classes.td}>{user.id}</td>
                <td className={classes.td}>{user.username}</td>
                <td className={classes.td}>{user.created_at}</td>
                <td className={classes.td}><Button title={"UPDATE"}/></td>
                <td className={classes.td}><Button title={"DELETE"} onClick={() => props.delFunc(user.id)}/></td>
            </tr>
        )
        return list;
    })
    const content = (
        <div>
            <h1>Existing Users</h1>
            <table className={classes.table}>
                <tbody>
                    {table}
                </tbody>
            </table>
        </div>
    )
    return (
        <Card content={content}/>
    );
}

export default Users;