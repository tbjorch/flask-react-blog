# standard library
from typing import Dict, List

# 3rd party modules
from flask import Response
from werkzeug.exceptions import NotFound

# Internal modules
from app.controllers.BaseController import BaseController
from app.models import Blogpost


class BlogpostController(BaseController):

    def create_blogpost(self, id) -> Response:
        data: Dict = self.get_required_data_from_request("headline", "body")
        post: Blogpost = Blogpost(data["headline"], data["body"], id)
        post.save()
        return self.make_json_response(
            dict(message="Blogpost successfully created")
            )

    def find_all(self) -> Response:
        blogposts: List[Blogpost] = Blogpost.find_all()
        if blogposts == []:
            raise NotFound("No blogposts exist")
        json_list: List[Dict] = [dict(
                blogpost.to_dict(),
                user=blogpost.user.to_dict()
                ) for blogpost in blogposts]
        return self.make_json_response(json_list)

    def find_by_id(self, id) -> Response:
        blogpost: Blogpost = Blogpost.find_by_id(id)
        if blogpost is None:
            raise NotFound(f"No blogpost found with id={id}")
        resp_dict = blogpost.to_dict()
        resp_dict.update(user=blogpost.user.to_dict())
        return self.make_json_response([resp_dict])

    def delete_blogpost(self, id) -> Response:
        post: Blogpost = Blogpost.find_by_id(id)
        if post is None:
            raise NotFound(f"No blogpost found with id={id}")
        post.delete()
        return self.make_json_response(
            dict(message="Blogpost successfully deleted")
            )
