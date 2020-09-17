import React from "react";
import Blogpost from "./Blogpost";

const Blogposts = (props) => {

    return props.blogposts.map((blogpost) => {
        return <Blogpost
            isLoggedIn={props.isLoggedIn}
            key={blogpost.id}
            title={blogpost.headline}
            body={blogpost.body}
            created={blogpost.created_at}
            author={blogpost.user.username}
            deletePost={() => props.delete(blogpost.id)}
            />
    });

}
export default Blogposts;