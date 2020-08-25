import React, { useState } from 'react';
import Card from '../UI/Card/Card';
import classes from './Users.module.css';

const Users = () => {
    const [users, setUsers] = useState([
        {id:1, username: "John", roles: "ADMIN, USER", joined: "2020-03-04 12:56", status: "ACTIVE"},
        {id:2, username: "Jessica", roles: "GLOBAL ADMIN", joined: "2020-05-13 22:22", status: "BANNED"},
        {id:3, username: "Prahalad", roles: "USER", joined: "2020-01-31 11:34", status: "INACTIVE"},
        {id:4, username: "Hamel", roles: "USER", joined: "2020-03-20 12:19", status: "ACTIVE"},
        {id:5, username: "Jesus", roles: "USER", joined: "2020-02-29 06:35", status: "INACTIVE"},
    ])
    const table= users.map((user) => {
        const content = (
            <tr className={classes.tr}>
                <td className={classes.td}>{user.id}</td>
                <td className={classes.td}>{user.username}</td>
                <td className={classes.td}>{user.roles}</td>
                <td className={classes.td}>{user.joined}</td>
                <td className={classes.td}>{user.status}</td>
                <td className={classes.td}><button>ÄNDRA</button></td>
                <td className={classes.td}><button>TA BORT</button></td>
            </tr>
        )
        return content;
    })
    return (
        <div>
            <table className={classes.table}>
                {table}
            </table>
        </div>
    );
}

export default Users;