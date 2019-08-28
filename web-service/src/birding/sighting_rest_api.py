from flask import Blueprint


def create_sighting_rest_api_blueprint() -> Blueprint:
  blueprint = Blueprint('v2sighting', __name__, url_prefix='/v2/sighting')

  return blueprint
