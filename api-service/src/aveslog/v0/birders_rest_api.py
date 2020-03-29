from http import HTTPStatus

from flask import g, make_response, jsonify, request

from aveslog.v0.birder_connections_rest_api import get_birder_connections
from aveslog.v0.birder_connections_rest_api import post_birder_connection
from aveslog.v0.birder_connections_rest_api import BirderConnectionDeleter
from aveslog.v0.models import Birder
from aveslog.v0.rest_api import require_authentication, cache


@cache(max_age=300)
@require_authentication
def get_birder(birder_id: int):
  birder = g.database_session.query(Birder).get(birder_id)
  if not birder:
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response(jsonify(birder_representation(birder)), HTTPStatus.OK)


@require_authentication
def get_birders_birder_connections(birder_id: int):
  return get_birder_connections(birder_id)


@require_authentication
def post_birders_birder_connection(birder_id: int):
  return post_birder_connection(birder_id)


@require_authentication
def delete_birders_birder_connection(birder_id: int, birder_connection_id: int):
  session = g.database_session
  account = g.authenticated_account
  deleter = BirderConnectionDeleter(session, account)
  return deleter.delete(birder_id, birder_connection_id)


@require_authentication
def get_birders():
  birders = g.database_session.query(Birder).all()
  json = jsonify({
    'items': list(map(birder_representation, birders)),
    'hasMore': False,
  })
  return make_response(json, HTTPStatus.OK)


def birder_representation(birder: Birder) -> dict:
  return {
    'id': birder.id,
    'name': birder.name,
  }
