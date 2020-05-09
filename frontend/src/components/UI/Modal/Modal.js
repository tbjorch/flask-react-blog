import React from 'react';
import classes from './Modal.module.css';

const Modal = (props) => {
    return (
        <div className={ classes.Modal } clicked={props.clicked} >
            { props.element }
        </div>
    )
}

export default Modal;