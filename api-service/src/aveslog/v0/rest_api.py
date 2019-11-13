from http import HTTPStatus


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
