import React from 'react';
import Button from '../UI/Button/Button';
import Card from '../UI/Card/Card';
import classes from './Blogpost.module.css';


const Blogpost = (props) => {
    const buttons = () => {
        return props.isLoggedIn ? (
            <div>
                <Button onClick={() => {props.deletePost(props.id)}} title="DELETE" />
            </div>
        ) : null;
    }

    const content = (
        <div>
            <div>
                <h1 className={classes.title}>
                    {props.title}
                </h1>
                <p className={classes.body}>
                    {props.body}
                </p>
            </div>
            <div className={classes.metadata}>
                <span className={classes.span}>
                    author: {props.author}
                </span>
                <span className={classes.span}>
                    {props.created}
                </span>
            </div>
            {buttons()}
        </div>
        
    );
    return <Card content={content} />;
}

export default Blogpost;