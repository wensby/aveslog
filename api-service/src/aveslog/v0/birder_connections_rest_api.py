from http import HTTPStatus

from flask import make_response
from flask import g
from flask import jsonify

from aveslog.v0.rest_api import require_authentication
from aveslog.v0.models import BirderConnection


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


def birder_connection_representation(connection: BirderConnection) -> dict:
  return {
    'id': connection.id,
    'secondaryBirderId': connection.secondary_birder_id,
  }
