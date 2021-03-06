import React, { useState } from 'react';
import Button from '../UI/Button/Button';
import axios from 'axios';
import Card from '../UI/Card/Card';

axios.defaults.withCredentials = true;

const BlogpostForm = (props) => {
    const [blogpost, setBlogpost] = useState({'headline':"", 'body':""});

    const titleChangeHandler = (event) => {
        const newBlogpost = {...blogpost};
        newBlogpost.headline = event.target.value;
        setBlogpost(newBlogpost);
    }

    const bodyChangeHandler = (event) => {
        const newBlogpost = {...blogpost};
        newBlogpost.body = event.target.value;
        setBlogpost(newBlogpost);
    }

    const create = (blogpost) => {
        axios.post("http://127.0.0.1:8080/api/v1/blogposts", blogpost, {
            withCredentials: true,
            headers: {
                "Content-Type": 'application/json'
            }
        }).then(response => {
            props.create(blogpost);
            setBlogpost({headline: "", body: ""});
            console.log(response.data.message);
        })
    }

    const content = (
        <div>
            <form>
                <h1>Add Blogpost Form</h1>
                <input value={blogpost.headline} onChange={event => titleChangeHandler(event)} placeholder="Blogpost Title" type="text"/>
                <textarea value={blogpost.body} onChange={event => bodyChangeHandler(event)} placeholder="Blogpost body text"/>
            </form>
            <Button onClick={() => create(blogpost)} title="PUBLISH" />
        </div>
    )

    return <Card content={content}/>
}

export default BlogpostForm;