# Standard library
from typing import Dict

# 3rd party modules
from flask import request, make_response, Response, jsonify
from werkzeug.exceptions import BadRequest


class BaseController():

    def get_required_data_from_request(self, *required_fields: str) -> Dict:
        """Checks request body for required data to be posted and returns
        as a dict. Throws BadRequest if request is not in json format,
        or if required field is missing or if request contains
        additional invalid fields."""
        if not request.is_json:
            raise BadRequest("Posted data is expected to be in JSON format")
        else:
            data = request.get_json()
            if len(data) != len(required_fields):
                raise BadRequest(
                    f"Expected {len(required_fields)}"
                    f" fields but got {len(data)}"
                    )
            for field in required_fields:
                if field not in data:
                    raise BadRequest(
                        f"Required field {field} is missing in request body"
                        )
            return data

    def get_required_params_from_request(self, *required_params: str) -> Dict:
        """Checks request for required params and returns them
        as a dict. Throws BadRequest if required param is missing """
        data = dict()
        for param in required_params:
            data[param] = request.args.get(param)
            if data[param] is None:
                raise BadRequest("Expected param is missing in request")
        return data

    def ok_response(self) -> Response:
        return make_response(jsonify(message="ok"), 200)

    def make_json_response(self, return_data: Dict) -> Response:
        response = make_response(jsonify(return_data), 200)
        response.content_type = "application/json"
        return response
