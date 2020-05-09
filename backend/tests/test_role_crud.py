# Standard library
import json

# Internal modules
from tests import CustomTestClient
from app.models import Role
from app import db


def test_post_role_correct() -> None:
    with CustomTestClient() as c:
        role = dict(
            name="ADMIN",
            description="Administrator role for the site"
        )
        res = c.post(
            '/roles',
            data=json.dumps(role),
            content_type="application/json"
            )
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "Role successfully created"
        role_record = Role.find_by_id(1)
        assert role_record.name == "ADMIN"
        assert role_record.description == "Administrator role for the site"


def test_post_role_already_exists() -> None:
    role: Role = Role("ADMIN", "Administrator role for the site")
    with CustomTestClient() as c:
        db.session.add(role)
        db.session.commit()
        role = dict(
            name="ADMIN",
            description="Administrator role for the site"
        )
        res = c.post(
            '/roles',
            data=json.dumps(role),
            content_type="application/json"
            )
        assert res.status_code == 400
        data = res.get_json()
        assert data["message"] == "Role with provided name already exists"


def test_post_role_badrequest_missing_required_field() -> None:
    with CustomTestClient() as c:
        role = dict(
            name="ADMIN",
            descripti="this key is incorrect"
        )
        res = c.post(
            '/roles',
            data=json.dumps(role),
            content_type="application/json"
            )
        assert res.status_code == 400
        data = res.get_json()
        assert data["message"] == \
            "Required field description is missing in request body"


def test_post_role_badrequest_not_json() -> None:
    with CustomTestClient() as c:
        role = dict(
            name="ADMIN",
            description="Administrator role for the site"
        )
        res = c.post(
            '/roles',
            data=json.dumps(role)
            )
        assert res.status_code == 400
        data = res.get_json()
        assert data["message"] == \
            "Posted data is expected to be in JSON format"


def test_get_role_by_id_correct() -> None:
    role: Role = Role("ADMIN", "Administrator role for the site")
    with CustomTestClient() as c:
        db.session.add(role)
        db.session.commit()
        res = c.get('/roles/1')
        assert res.status_code == 200
        data = res.get_json()
        assert data["name"] == "ADMIN"
        assert data["description"] == "Administrator role for the site"


def test_get_role_by_id_nonexisting() -> None:
    with CustomTestClient() as c:
        res = c.get('/roles/1')
        assert res.status_code == 404
        data = res.get_json()
        assert data["message"] == "No role found with provided id"


def test_get_role_by_name_correct() -> None:
    role: Role = Role("ADMIN", "Administrator role for the site")
    with CustomTestClient() as c:
        db.session.add(role)
        db.session.commit()
        res = c.get('/roles?name=ADMIN')
        assert res.status_code == 200
        data = res.get_json()
        assert data["name"] == "ADMIN"
        assert data["description"] == "Administrator role for the site"


def test_get_role_by_name_nonexisting() -> None:
    with CustomTestClient() as c:
        res = c.get('/roles?name=ADMIN')
        assert res.status_code == 404
        data = res.get_json()
        assert data["message"] == "No role found with provided name"


def test_delete_role_correct() -> None:
    role: Role = Role("ADMIN", "Administrator role for the site")
    with CustomTestClient() as c:
        db.session.add(role)
        db.session.commit()
        res = c.delete('/roles/1')
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "Role successfully deleted"


def test_delete_role_nonexisting() -> None:
    with CustomTestClient() as c:
        res = c.delete('/roles/1')
        assert res.status_code == 404
        data = res.get_json()
        assert data["message"] == "No role found with provided id"
