import React from 'react';
import classes from './Select.module.css';

const Select = (props) => {
    const options = props.options.map((option) => {
        return (
            <option value={option.value}>{option.value.charAt(0).toUpperCase(0) + option.value.slice(1)}</option>
        )
    })
    return (
        <div>
            <label className={classes.smallLabel}><h2>{props.label}</h2></label>
            <select className={classes.small} name={props.name} id={props.name} onChange={(event) => props.onChange(event)} value={props.value}>
                <option value="---">---</option>
                {options}
            </select>
        </div>
    )
}

export default Select;