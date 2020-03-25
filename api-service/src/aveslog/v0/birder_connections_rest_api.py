from http import HTTPStatus
from typing import Optional

from flask import make_response
from flask import Response
from flask import g
from flask import jsonify
from sqlalchemy.orm import Session, joinedload

from aveslog.v0.rest_api import require_authentication
from aveslog.v0.models import BirderConnection
from aveslog.v0.models import Birder
from aveslog.v0.models import Account


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


class BirderConnectionsGetter:

  def __init__(self, account):
    self._account: Account = account

  def get(self, birder_id: int) -> Response:
    if self._account.birder_id != birder_id:
      return make_response('', HTTPStatus.UNAUTHORIZED)
    birder = g.database_session.query(Birder) \
      .options(joinedload(Birder.connections)) \
      .get(birder_id)
    if not birder:
      return make_response('', HTTPStatus.NOT_FOUND)
    return make_response(jsonify({
      'items': list(map(birder_connection_representation, birder.connections)),
      'hasMore': False
    }), HTTPStatus.OK)


class BirderConnectionPoster:

  def __init__(self, database_session, account):
    self._db: Session = database_session
    self._account: Account = account

  def post(self, birder_id: int, secondary_birder_id) -> Response:
    if not secondary_birder_id or not isinstance(secondary_birder_id, int):
      return make_response('', HTTPStatus.BAD_REQUEST)
    if secondary_birder_id == birder_id:
      return make_response('', HTTPStatus.BAD_REQUEST)
    if self._account.birder_id != birder_id:
      return make_response('', HTTPStatus.UNAUTHORIZED)
    if not self._db.query(Birder).get(birder_id):
      return make_response('', HTTPStatus.NOT_FOUND)
    if self.is_connection_present(birder_id, secondary_birder_id):
      return make_response('', HTTPStatus.CONFLICT)
    birder_connection = BirderConnection(
      primary_birder_id=birder_id,
      secondary_birder_id=secondary_birder_id,
    )
    self._db.add(birder_connection)
    self._db.commit()
    response = make_response('', HTTPStatus.CREATED)
    response.headers['Location'] = f'/birder-connections/{birder_connection.id}'
    response.autocorrect_location_header = False
    return response

  def is_connection_present(self, primary_birder_id, secondary_birder_id):
    connection = self._db.query(BirderConnection) \
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
