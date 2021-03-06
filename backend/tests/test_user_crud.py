# standard library
import json

# internal modules
from tests import CustomTestClient
from app.models import User, Role
from app.controllers.AuthController import AuthController

auth = AuthController.get_instance()


def test_post_user_already_exists() -> None:
    with CustomTestClient() as c:
        User("hauck", "asd123").save()
        user = {"username": "hauck", "password": "qwe123"}
        res = c.post(
            '/api/v1/users',
            data=json.dumps(user),
            content_type="application/json")
        assert res.status_code == 400
        data = res.get_json()
        assert data["message"] == "Username is already taken"


def test_post_user_correct() -> None:
    with CustomTestClient() as c:
        user = dict(username="hauck", password="qwe123")
        res = c.post(
            '/api/v1/users',
            data=json.dumps(user),
            content_type="application/json")
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "User successfully created"


def test_get_user_by_id_correct() -> None:
    with CustomTestClient() as c:
        User("hauck", "asd123").save()
        res = c.get('/api/v1/users/1')
        assert res.status_code == 200
        data = res.get_json()
        assert data['username'] == "hauck"
        assert data['id'] == 1


def test_get_user_by_id_nonexisting_user() -> None:
    with CustomTestClient() as c:
        res = c.get('/api/v1/users/1')
        assert res.status_code == 404
        data = res.get_json()
        assert data['message'] == "No user found with id=1"


def test_get_user_by_id_nonexisting_user_and_bad_id() -> None:
    with CustomTestClient() as c:
        res = c.get('/api/v1/users/asd')
        assert res.status_code == 404
        data = res.get_json()
        assert data['message'] == "No user found with id=asd"


def test_delete_user_correct() -> None:
    with CustomTestClient() as c:
        User("hauck", "asd123").save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete('/api/v1/users/1')
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "User successfully deleted"


def test_delete_user_non_existing() -> None:
    with CustomTestClient() as c:
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete('/api/v1/users/1')
        assert res.status_code == 404
        data = res.get_json()
        assert data["message"] == "No user found with id=1"


def test_delete_user_non_existing_and_bad_id() -> None:
    with CustomTestClient() as c:
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete('/api/v1/users/1')
        assert res.status_code == 404
        data = res.get_json()
        assert data["message"] == "No user found with id=1"


def test_post_user_role_correct() -> None:
    with CustomTestClient() as c:
        User("jane", "asd123").save()
        User("JOHN", "asd123").save()
        User("Leia", "asd123").save()
        Role("ADMIN", "Administrator for site").save()
        Role("FINANCE", "financer for site").save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.post(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )
        res_2 = c.post(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'FINANCE'}),
            content_type='application/json'
        )
        res_3 = c.post(
            '/api/v1/users/3/roles',
            data=json.dumps({'role': 'FINANCE'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data['message'] == "Role successfully added to user"
        assert res.status_code == 200
        data_2 = res_2.get_json()
        assert data_2['message'] == "Role successfully added to user"
        assert res_2.status_code == 200
        data_3 = res_3.get_json()
        assert data_3['message'] == "Role successfully added to user"
        assert res_3.status_code == 200
        user_1 = User.find_by_id(1)
        assert user_1.roles[0].name == "ADMIN"
        assert user_1.roles[0].description == "Administrator for site"
        assert user_1.roles[1].name == "FINANCE"
        assert user_1.roles[1].description == "financer for site"
        user_2 = User.find_by_id(2)
        assert user_2.roles == []
        user_3 = User.find_by_id(3)
        assert user_3.roles[0].name == "FINANCE"
        assert user_3.roles[0].description == "financer for site"


def test_post_user_role_nonexisting_role() -> None:
    with CustomTestClient() as c:
        User("jane", "asd123").save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.post(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'URHMA'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data['message'] == "No role found with name=URHMA"
        assert res.status_code == 404


def test_post_user_role_nonexisting_user() -> None:
    with CustomTestClient() as c:
        Role("ADMIN", "Administrator for site").save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.post(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data['message'] == "No user found with id=1"
        assert res.status_code == 404


def test_delete_user_role_not_authorized_not_logged_in() -> None:
    with CustomTestClient() as c:
        res = c.delete(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data["message"] == "You need to be signed in"
        assert res.status_code == 401


def test_delete_user_role_not_authorized_role() -> None:
    with CustomTestClient() as c:
        token = auth.create_jwt_token("JohnDoe", 1, ["UNAUTHORIZED_ROLE"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data["message"] == \
            "You are not authorized to perform this action"
        assert res.status_code == 401


def test_delete_user_role_nonexisting_user() -> None:
    with CustomTestClient() as c:
        Role("USER", "User on site").save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'USER'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data['message'] == "No user found with id=1"
        assert res.status_code == 404


def test_delete_user_role_nonexisting_role() -> None:
    with CustomTestClient() as c:
        User("jane", "asd123").save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data['message'] == "No role found with name=ADMIN"
        assert res.status_code == 404


def test_delete_user_role_correct() -> None:
    with CustomTestClient() as c:
        role = Role("ADMIN", "Administrator for site")
        role.save()
        user = User("jane", "asd123")
        user.roles.append(role)
        user.save()
        token = auth.create_jwt_token("JohnDoe", 1, ["ADMIN"])
        c.set_cookie('localhost:5000', 'Authorization', token)
        res = c.delete(
            '/api/v1/users/1/roles',
            data=json.dumps({'role': 'ADMIN'}),
            content_type='application/json'
        )
        data = res.get_json()
        assert data['message'] == "Role successfully deleted from user"
        assert res.status_code == 200
        user_1 = User.find_by_id(1)
        assert user_1.roles == []
