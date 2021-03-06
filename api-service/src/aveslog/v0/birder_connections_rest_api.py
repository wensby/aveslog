from http import HTTPStatus
from typing import Optional

from flask import make_response
from flask import request
from flask import Response
from flask import g
from flask import jsonify
from sqlalchemy.orm import Session

from aveslog.v0.error import ErrorCode
from aveslog.v0.rest_api import require_authentication
from aveslog.v0.rest_api import validation_failed_error_response
from aveslog.v0.models import BirderConnection
from aveslog.v0.models import Birder
from aveslog.v0.models import Account

secondary_birder_id_key = 'secondaryBirderId'


@require_authentication
def get_birder_connection(birder_connection_id: int):
  db_session = g.database_session
  account = g.authenticated_account
  connection = db_session.query(BirderConnection).get(birder_connection_id)
  if not connection or connection.primary_birder_id != account.birder_id:
    # making sure to hide existence of unauthorized resources
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response(
    jsonify(birder_connection_representation(connection)),
    HTTPStatus.OK
  )


@require_authentication
def delete_birder_connection(birder_connection_id: int):
  session = g.database_session
  account = g.authenticated_account
  deleter = BirderConnectionDeleter(session, account)
  return deleter.delete(None, birder_connection_id)


def birder_connection_representation(connection: BirderConnection) -> dict:
  return {
    'id': connection.id,
    'secondaryBirderId': connection.secondary_birder_id,
  }


def get_birder_connections(birder_id: int) -> Response:
  account = g.authenticated_account
  if account.birder_id != birder_id:
    return make_response('', HTTPStatus.UNAUTHORIZED)
  connections = account.birder.connections
  return make_response(jsonify({
    'items': list(map(birder_connection_representation, connections)),
    'hasMore': False
  }), HTTPStatus.OK)


def post_birder_connection(birder_id: int) -> Response:
  secondary_birder_id = request.json.get(secondary_birder_id_key)
  field_errors = validate_fields(birder_id, secondary_birder_id)
  if field_errors:
    return validation_failed_error_response(field_errors)
  if g.authenticated_account.birder_id != birder_id:
    return make_response('', HTTPStatus.UNAUTHORIZED)
  if not g.database_session.query(Birder).get(birder_id):
    return make_response('', HTTPStatus.NOT_FOUND)
  if is_connection_present(birder_id, secondary_birder_id):
    return make_response('', HTTPStatus.CONFLICT)
  birder_connection = BirderConnection(
    primary_birder_id=birder_id,
    secondary_birder_id=secondary_birder_id,
  )
  g.database_session.add(birder_connection)
  g.database_session.commit()
  response = make_response('', HTTPStatus.CREATED)
  response.headers['Location'] = f'/birder-connections/{birder_connection.id}'
  response.autocorrect_location_header = False
  return response


def validate_fields(primary_birder_id, secondary_birder_id) -> list:
  errors = []
  if not present_int(secondary_birder_id):
    errors.append({
      'code': ErrorCode.INVALID_FIELD_FORMAT,
      'field': secondary_birder_id_key,
      'message': 'Identifier need to be a positive integer',
    })
  elif secondary_birder_id == primary_birder_id:
    errors.append({
      'code': ErrorCode.SECONDARY_BIRDER_ID_INVALID,
      'field': secondary_birder_id_key,
      'message': 'Birder may not create connection with itself',
    })
  return errors


def present_int(value) -> bool:
  return value and isinstance(value, int)


def is_connection_present(primary_birder_id, secondary_birder_id):
  connection = g.database_session.query(BirderConnection) \
    .filter_by(primary_birder_id=primary_birder_id) \
    .filter_by(secondary_birder_id=secondary_birder_id) \
    .first()
  return connection is not None


class BirderConnectionDeleter:

  def __init__(self, database_session, account):
    self._db: Session = database_session
    self._account: Account = account

  def delete(self, birder_id: Optional[int], connection_id: int) -> Response:
    account_birder_id = self._account.birder_id
    if birder_id and account_birder_id != birder_id:
      return make_response('', HTTPStatus.UNAUTHORIZED)
    connection = self._db.query(BirderConnection).get(connection_id)
    if not connection or connection.primary_birder_id != account_birder_id:
      # making sure to hide existence of unauthorized resources
      return make_response('', HTTPStatus.NOT_FOUND)
    self._db.delete(connection)
    self._db.commit()
    return make_response('', HTTPStatus.NO_CONTENT)
