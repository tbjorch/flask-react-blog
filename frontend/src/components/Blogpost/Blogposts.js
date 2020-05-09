import React from "react";
import Blogpost from "./Blogpost";

const Blogposts = (props) => {

    return props.blogposts.map((blogpost) => {
        return <Blogpost
            isLoggedIn={props.isLoggedIn}
            key={blogpost.id}
            title={blogpost.headline}
            body={blogpost.body}
            deletePost={() => props.delete(blogpost.id)}
            />
    });

}
export default Blogposts;