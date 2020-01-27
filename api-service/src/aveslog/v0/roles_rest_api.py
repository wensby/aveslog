from http import HTTPStatus

from flask import Response, jsonify, make_response, g

from aveslog.v0.models import Role
from aveslog.v0.rest_api import cache


@cache(max_age=300)
def get_role_permissions(role_id: str) -> Response:
  role = g.database_session.query(Role).filter_by(name=role_id).first()
  json = jsonify({'id': role.id, 'name': role.name})
  return make_response(json, HTTPStatus.OK)
