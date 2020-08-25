import React, {useState, useEffect} from 'react';
import './App.css';

import Blogposts from '../components/Blogpost/Blogposts';
import BlogpostForm from '../components/Blogpost/BlogpostForm';
import LoginForm from '../components/Login/LoginForm';
import RegisterForm from '../components/Register/RegisterForm';
import Profile from '../components/Profile/Profile';
import NavBar from '../components/NavBar/NavBar';
import styled from "styled-components";
import axios from 'axios';
import UserContainer from './UserContainer';

const MainContainer = styled.div`
    width: 85%;
    margin: auto;
`

const BlogpostContainer = styled.div`
    display: flex;
    flex-flow: row wrap;
    `

function App() {

  const [blogposts, setBlogposts] = useState([]);
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  useEffect(() => {
    if(blogposts.length === 0){
      axios.get("http://127.0.0.1:8080/api/v1/blogposts").then(response => {
        setBlogposts(response.data);
      })
    }
  })

  const [activeLink, setActivelink] = useState("/users");
  const [credentials, setCredentials] = useState(false);

  const deleteBlogpost = (postId) => {
    axios.delete("http://127.0.0.1:8080/api/v1/blogposts/"+postId).then(response => {
      const arrayIndex = blogposts.findIndex(post => post.id==postId);
      const updatedBlogposts = [...blogposts];
      updatedBlogposts.splice(arrayIndex, 1);
      setBlogposts(updatedBlogposts);
    }
    )
  }

  const duplicateBlogpost = (index) => {
    const posts = [...blogposts];
    posts.push(blogposts[index]);
    setBlogposts(posts);
  }

  const onLinkClick = (linkValue) => {
    const newLink = linkValue;
    setActivelink(newLink);
  }

  const onAddBlogpost = (newPost) => {
    const updatedBlogpostList = [...blogposts, newPost];
    console.log(updatedBlogpostList);
    setBlogposts(updatedBlogpostList);
  }

  const loginHandler = (credentials) => {
    axios.post("http://127.0.0.1:8080/api/v1/login", credentials, {
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => {
        setCredentials(true);
        alert(response.data.message);
        setShowLogin(false);
        onLinkClick("/");
    }).catch(error => {
      alert("ERROR " + error.response.data.code + " " + error.response.data.message);
    })
  }

  const logoutHandler = () => {
    setCredentials(false);
    onLinkClick("/");
  }

  const registerHandler = (credentials) => {
    axios.post("http://127.0.0.1:8080/api/v1/users", credentials, {
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => {
      alert(response.data.message);
      setShowRegister(false);
      onLinkClick("/");
    })
  }

  const Content = () => {
    if (activeLink === "/" || activeLink === "/blog") {
      return (
        <BlogpostContainer>
          <Blogposts isLoggedIn={credentials} blogposts={blogposts} delete={deleteBlogpost} duplicate={duplicateBlogpost}/>
        </BlogpostContainer>
      );
    } else if (activeLink === "/add-blogpost") {
      return <BlogpostForm create={onAddBlogpost} />
    } else if (activeLink === "/profile") {
      return <Profile />
    } else if (activeLink === "/login") {
      return null;
    } else if (activeLink === "/register") {
      return null;
    } else if (activeLink === "/users") {
      return <UserContainer/>
    }
  }

  return (
    <div className="App">
      <NavBar loggedIn={credentials} active={onLinkClick} register={() => setShowRegister(true)} login={() => setShowLogin(true)} logout={() => logoutHandler()}/>
      <MainContainer>
        <Content/>
      </MainContainer>
      {showLogin ? <LoginForm login={loginHandler} show={() => setShowLogin()} /> : null }
      {showRegister ? <RegisterForm register={registerHandler} show={() => setShowRegister()} /> : null }
    </div>
  );
}

export default App;
