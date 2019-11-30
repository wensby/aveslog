from http import HTTPStatus

from flask import Response, make_response, jsonify


def error_response(
      error_code: int,
      message: str,
      additional_errors: list = None,
      status_code: int = HTTPStatus.BAD_REQUEST,
) -> Response:
  data = {
    'code': error_code,
    'message': message,
  }
  if additional_errors:
    data['errors'] = additional_errors
  return make_response(jsonify(data), status_code)
