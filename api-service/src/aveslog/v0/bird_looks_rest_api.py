from http import HTTPStatus

from flask import g, make_response, jsonify
from sqlalchemy.orm import joinedload

from aveslog.v0.models import BirdLook
from aveslog.v0.rest_api import cache


@cache(max_age=300)
def get_bird_look(bird_look_id: int):
  bird_look = g.database_session.query(BirdLook) \
    .options(joinedload(BirdLook.bird)) \
    .get(bird_look_id)
  if not bird_look:
    return make_response('', HTTPStatus.NOT_FOUND)
  return make_response(jsonify(bird_look_representation(bird_look)),
    HTTPStatus.OK)


def bird_look_representation(bird_look: BirdLook) -> dict:
  return {
    'id': bird_look.id,
    'birdId': bird_look.bird.binomial_name.lower().replace(' ', '-'),
    'label': bird_look.label,
    'description': bird_look.description,
  }
