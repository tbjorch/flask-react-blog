import React from 'react';
import classes from './MainContainer.module.css';

const MainContainer = (props) => (
    <div className={classes.main}>
        {props.content}
    </div>
)

export default MainContainer;