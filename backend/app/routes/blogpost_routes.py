# 3rd party modules
from flask import Response, request

# Internal modules
from app import app
from app.controllers import BlogpostController, AuthController


controller: BlogpostController = BlogpostController()
auth = AuthController.get_instance()


@app.route('/api/v1/health')
def hello_world() -> Response:
    return "Ok!"


@app.route('/api/v1/blogposts', methods=['POST'])
@auth.authorize(["ADMIN"])
def create_blogpost() -> Response:
    token = request.cookies.get("Authorization")
    token_data = auth.decode_jwt_token(token)
    return controller.create_blogpost(token_data["user_id"])


@app.route('/api/v1/blogposts', methods=['GET'])
def find_all() -> Response:
    return controller.find_all()


@app.route('/api/v1/blogposts/<id>', methods=['GET'])
def find_blogpost(id) -> Response:
    return controller.find_by_id(id)


@app.route('/api/v1/blogposts/<id>', methods=['DELETE'])
@auth.authorize(["ADMIN"])
def delete_blogpost(id) -> Response:
    return controller.delete_blogpost(id)
