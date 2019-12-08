from aveslog.v0 import accounts_rest_api
from aveslog.v0 import registration_requests_rest_api
from aveslog.v0 import birds_rest_api
from aveslog.v0 import search_api
from aveslog.v0 import authentication_rest_api
from aveslog.v0 import sightings_rest_api
from aveslog.v0 import birders_rest_api


def create_birds_routes():
  routes = [
    {
      'rule': '/birds/<string:bird_identifier>',
      'func': birds_rest_api.get_single_bird,
    },
  ]

  return routes


def create_search_routes() -> list:
  return [
    {
      'rule': '/search/birds',
      'func': search_api.search_birds,
    }
  ]


def create_registration_requests_routes() -> list:
  return [
    {
      'rule': '/registration-requests',
      'func': registration_requests_rest_api.post_registration_request,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/registration-requests/<string:token>',
      'func': registration_requests_rest_api.get_registration_request,
    },
  ]


def create_account_routes() -> list:
  return [
    {
      'rule': '/accounts/<string:username>',
      'func': accounts_rest_api.get_account,
    },
    {
      'rule': '/accounts',
      'func': accounts_rest_api.create_account,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/accounts',
      'func': accounts_rest_api.get_accounts,
    },
    {
      'rule': '/account',
      'func': accounts_rest_api.get_me,
    },
    {
      'rule': '/account/password',
      'func': accounts_rest_api.post_password,
      'options': {'methods': ['POST']},
    },
  ]


def create_authentication_routes() -> list:
  return [
    {
      'rule': '/authentication/refresh-token',
      'func': authentication_rest_api.post_refresh_token,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/refresh-token/<int:refresh_token_id>',
      'func': authentication_rest_api.delete_refresh_token,
      'options': {'methods': ['DELETE']},
    },
    {
      'rule': '/authentication/access-token',
      'func': authentication_rest_api.get_access_token,
    },
    {
      'rule': '/authentication/password-reset',
      'func': authentication_rest_api.post_password_reset_email,
      'options': {'methods': ['POST']},
    },
    {
      'rule': '/authentication/password-reset/<string:token>',
      'func': authentication_rest_api.post_password_reset,
      'options': {'methods': ['POST']},
    },
  ]


def create_sightings_routes() -> list:
  return [
    {
      'rule': '/birders/<int:birder_id>/sightings',
      'func': sightings_rest_api.get_birder_sightings,
    },
    {
      'rule': '/sightings',
      'func': sightings_rest_api.get_sightings,
    },
    {
      'rule': '/sightings/<int:sighting_id>',
      'func': sightings_rest_api.get_sighting,
    },
    {
      'rule': '/sightings/<int:sighting_id>',
      'func': sightings_rest_api.delete_sighting,
      'options': {'methods': ['DELETE']},
    },
    {
      'rule': '/sightings',
      'func': sightings_rest_api.post_sighting,
      'options': {'methods': ['POST']},
    },
  ]
  pass


def create_birders_routes() -> list:
  return [
    {
      'rule': '/birders/<int:birder_id>',
      'func': birders_rest_api.get_birder,
    },
  ]
