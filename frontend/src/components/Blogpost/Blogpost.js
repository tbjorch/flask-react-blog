import React from 'react';
import Button from '../UI/Button/Button';
import Card from '../UI/Card/Card';


const Blogpost = (props) => {
    const buttons = () => {
        return props.isLoggedIn ? (
            <div>
                <Button onClick={() => {props.deletePost(props.id)}} title="DELETE" />
                <Button onClick={() => {props.duplicatePost(props.id)}} title="DUPLICATE" />
            </div>
        ) : null;
    }

    const content = (
        <div>
            <h1>
                {props.title}
            </h1>
            <p>
                {props.body}
            </p>
            {buttons()}
        </div>
    );
    return <Card content={content} />;
}

export default Blogpost;