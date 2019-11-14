from http import HTTPStatus

from flask import Response, make_response, jsonify


class RestApiResponse:

  def __init__(self, status: int, data: dict):
    self.status = status
    self.data = data


def error_response(
      error_code: int,
      message: str,
      status_code: int = HTTPStatus.BAD_REQUEST,
) -> RestApiResponse:
  return RestApiResponse(status_code, {
    'code': error_code,
    'message': message,
  })


def create_flask_response(response: RestApiResponse) -> Response:
  return make_response(jsonify(response.data), response.status)
