import React from 'react';
import classes from './Button.module.css';

const Button = (props) => {
return <button className={classes.button} onClick={() => props.onClick()}> {props.title} </button>
}

export default Button;