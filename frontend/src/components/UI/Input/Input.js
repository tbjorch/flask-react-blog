import React from 'react';
import classes from './Input.module.css';

const Input = (props) => {

    if (props.label) {
        return (
            <div>
                <label className={classes.smallLabel}><h2>{props.label}</h2></label>
                <input 
                    className={classes.small}
                    type={props.type}
                    placeholder={props.placeholder}
                    value={props.value}
                    onChange={(event) => props.onChange(event)}/>
            </div>
        )
    } else {
        return <input className={classes.small} type={props.type} placeholder={props.placeholder}/>
    }
}
export default Input;