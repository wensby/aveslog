class RestApiResponse:

  def __init__(self, status: int, data: dict):
    self.status = status
    self.data = data