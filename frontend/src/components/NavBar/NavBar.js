import React from 'react';
import classes from './NavBar.module.css';

const NavBar = (props) => {
    let navBar;
    if(props.loggedIn) {
        navBar = (
            <div className={classes.navbar}>
                <span>
                    <button className={classes.navbarButton} key={1} onClick={() => props.active("/")} >BLOG</button>
                </span>
                <span className={classes.rightButtonGroup}  >
                    <button className={classes.navbarButton} key={2} onClick={() => props.active("/blog")} >Blog</button>
                    <button className={classes.navbarButton} key={3} onClick={() => props.active("/add-blogpost")} >Add blogpost</button>  
                    <button className={classes.navbarButton} key={4} onClick={() => props.active("/users")} >Users</button>  
                    <button className={classes.navbarButton} key={5} onClick={() => props.logout()}>Logout</button>
                </span>
            </div>
        );
    } else {
        navBar = (
            <div className={classes.navbar}>
                <span>
                    <button className={classes.navbarButton} key={1} onClick={() => props.active("/")} >BLOG</button>
                </span>
                <span className={classes.rightButtonGroup}>
                    <button className={classes.navbarButton} key={2} onClick={() => props.active("/blog")} >Blog</button>
                    <button className={classes.navbarButton} onClick={() => {props.login(true)}}>Login</button>
                    <button className={classes.navbarButton} onClick={() => {props.register(true)}}>Register</button>
                </span>
            </div>
        );
    }

    return navBar;
} 
export default NavBar;