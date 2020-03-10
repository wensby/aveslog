from http import HTTPStatus

from flask import g, make_response, jsonify

from aveslog.v0.models import Birder
from aveslog.v0.rest_api import require_authentication, cache


@cache(max_age=300)
@require_authentication
def get_birder(birder_id: int):
  birder = g.database_session.query(Birder).get(birder_id)
  if not birder:
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response(jsonify(convert_birder(birder)), HTTPStatus.OK)


@require_authentication
def get_birders():
  birders = g.database_session.query(Birder).all()
  json = jsonify({
    'items': list(map(convert_birder, birders)),
    'hasMore': False,
  })
  return make_response(json, HTTPStatus.OK)


def convert_birder(birder: Birder) -> dict:
  return {
    'id': birder.id,
    'name': birder.name,
  }
