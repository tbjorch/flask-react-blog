# Standard library
import json

# Internal modules
from tests import CustomTestClient
from app import db
from app.models import Blogpost, User

from app.controllers import AuthController

auth = AuthController.get_instance()


def test_post_blogposts_correct() -> None:
    user = User("jane", "asd123")
    with CustomTestClient() as c:
        db.session.add(user)
        db.session.commit()
        blogpost = {
            "headline": "This is my headline",
            "body": "This is my body"
            }
        res = c.post(
            '/blogposts',
            data=json.dumps(blogpost),
            content_type="application/json"
            )
        data = res.get_json()
        assert data["message"] == "Blogpost successfully created"
        assert res.status_code == 200
        blogpost_2 = {
            "headline": "This is my other headline",
            "body": "This is my second body text different from the first!"
            }
        res_2 = c.post(
            '/blogposts',
            data=json.dumps(blogpost_2),
            content_type="application/json"
            )
        data_2 = res_2.get_json()
        assert data_2["message"] == "Blogpost successfully created"
        assert res_2.status_code == 200
        user = User.find_by_username("jane")
        assert user.blogposts is not None
        assert user.blogposts[0].headline == "This is my headline"
        assert user.blogposts[0].body == "This is my body"
        assert user.blogposts[1].headline == "This is my other headline"
        assert user.blogposts[1].body == \
            "This is my second body text different from the first!"
        blogpost_1 = Blogpost.find_by_id(1)
        blogpost_2 = Blogpost.find_by_id(2)
        assert blogpost_1.author_id == blogpost_2.author_id == 1


def test_post_blogpost_badrequest_content_type_not_json() -> None:
    with CustomTestClient() as c:
        blogpost = {
            "headline": "This is my headline",
            "body": "This is my body"
            }
        res = c.post(
            '/blogposts',
            data=json.dumps(blogpost)
            )
        data = res.get_json()
        assert data["message"] == \
            "Posted data is expected to be in JSON format"
        assert res.status_code == 400


def test_post_blogpost_badrequest_missing_headline_field() -> None:
    with CustomTestClient() as c:
        blogpost = {
            "something": "Hello",
            "body": "This is my body"
            }
        res = c.post(
            '/blogposts',
            data=json.dumps(blogpost),
            content_type="application/json"
            )
        data = res.get_json()
        assert data["message"] == \
            "Required field headline is missing in request body"
        assert res.status_code == 400


def test_post_blogpost_badrequest_too_few_fields_in_json_request() -> None:
    with CustomTestClient() as c:
        blogpost = {
            "body": "This is my body"
            }
        res = c.post(
            '/blogposts',
            data=json.dumps(blogpost),
            content_type="application/json"
            )
        data = res.get_json()
        assert data["message"] == \
            "Expected 2 fields but got 1"
        assert res.status_code == 400


def test_delete_blogpost_not_logged_in() -> None:
    with CustomTestClient() as c:
        res = c.delete('/blogposts/1')
        data = res.get_json()
        assert data["message"] == \
            "You need to be logged in"
        assert res.status_code == 401


def test_delete_blogpost_unauthorized_role() -> None:
    with CustomTestClient() as c:
        token = auth.create_jwt_token("JohnDoe", 1, ["NON_AUTHORIZED_ROLE"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete('/blogposts/1')
        data = res.get_json()
        assert data["message"] == \
            "You are not authorized to perform this action"
        assert res.status_code == 401


def test_delete_blogpost_correct() -> None:
    with CustomTestClient() as c:
        blogpost: Blogpost = Blogpost("Headline", "Body", 1)
        db.session.add(blogpost)
        db.session.commit()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete('/blogposts/1')
        data = res.get_json()
        assert data["message"] == "Blogpost successfully deleted"
        assert res.status_code == 200


def test_delete_blogpost_nonexisting() -> None:
    with CustomTestClient() as c:
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete('/blogposts/1')
        data = res.get_json()
        assert data["message"] == "No blogpost found with id=1"
        assert res.status_code == 404


def test_get_blogpost_correct() -> None:
    with CustomTestClient() as c:
        blogpost: Blogpost = \
            Blogpost("This is my headline", "This is a body text", 1)
        db.session.add(blogpost)
        db.session.commit()
        res = c.get('/blogposts/1')
        data = res.get_json()
        assert data[0]["headline"] == "This is my headline"
        assert data[0]["body"] == "This is a body text"
        assert res.status_code == 200


def test_get_blogpost_nonexisting() -> None:
    with CustomTestClient() as c:
        res = c.get('/blogposts/1')
        data = res.get_json()
        assert data["message"] == "No blogpost found with id=1"
        assert res.status_code == 404
