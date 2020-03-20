from http import HTTPStatus

from flask import g, make_response, jsonify, request
from sqlalchemy.orm import joinedload

from aveslog.v0.birder_connections_rest_api import \
  birder_connection_representation
from aveslog.v0.birder_connections_rest_api import BirderConnectionDeleter
from aveslog.v0.models import Birder
from aveslog.v0.models import BirderConnection
from aveslog.v0.rest_api import require_authentication, cache


@cache(max_age=300)
@require_authentication
def get_birder(birder_id: int):
  birder = g.database_session.query(Birder).get(birder_id)
  if not birder:
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response(jsonify(convert_birder(birder)), HTTPStatus.OK)


@require_authentication
def get_birders_birder_connections(birder_id: int):
  account = g.authenticated_account
  if account.birder_id != birder_id:
    return make_response('', HTTPStatus.UNAUTHORIZED)
  birder = g.database_session.query(Birder).options(
    joinedload(Birder.connections)).get(birder_id)
  if not birder:
    return make_response('', HTTPStatus.NOT_FOUND)
  json = jsonify({
    'items': list(map(birder_connection_representation, birder.connections)),
    'hasMore': False
  })
  return make_response(json, HTTPStatus.OK)


@require_authentication
def post_birders_birder_connection(birder_id: int):
  account = g.authenticated_account
  db_session = g.database_session
  secondary_birder_id = request.json.get('secondaryBirderId')
  if not secondary_birder_id or not isinstance(secondary_birder_id, int) or secondary_birder_id == birder_id:
    return make_response('', HTTPStatus.BAD_REQUEST)
  if account.birder_id != birder_id:
    return make_response('', HTTPStatus.UNAUTHORIZED)
  primary_birder = db_session.query(Birder).get(birder_id)
  if not primary_birder:
    return make_response('', HTTPStatus.NOT_FOUND)
  if db_session.query(BirderConnection).filter_by(primary_birder_id=primary_birder.id).filter_by(secondary_birder_id=secondary_birder_id).first():
    return make_response('', HTTPStatus.CONFLICT)
  birder_connection = BirderConnection(primary_birder_id=primary_birder.id, secondary_birder_id=secondary_birder_id)
  db_session.add(birder_connection)
  db_session.commit()
  response = make_response('', HTTPStatus.CREATED)
  response.headers['Location'] = f'/birder-connections/{birder_connection.id}'
  response.autocorrect_location_header = False
  return response


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
    'items': list(map(convert_birder, birders)),
    'hasMore': False,
  })
  return make_response(json, HTTPStatus.OK)


def convert_birder(birder: Birder) -> dict:
  return {
    'id': birder.id,
    'name': birder.name,
  }
