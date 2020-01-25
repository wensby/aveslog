from http import HTTPStatus

from flask import Response, jsonify, make_response, g

from aveslog.v0.models import Locale
from aveslog.v0.rest_api import cache


@cache(max_age=300)
def get_locales() -> Response:
  locales = g.database_session.query(Locale).all()
  json = jsonify({'items': list(map(lambda l: l.code, locales))})
  return make_response(json, HTTPStatus.OK)
