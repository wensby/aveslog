from aveslog.v0 import accounts_rest_api
from aveslog.v0 import registration_requests_rest_api
from aveslog.v0 import birds_rest_api
from aveslog.v0 import search_api
from aveslog.v0 import authentication_rest_api
from aveslog.v0 import sightings_rest_api
from aveslog.v0 import birders_rest_api
from aveslog.v0 import locales_rest_api
from aveslog.v0 import roles_rest_api

birds_routes = [
  {
    'rule': '/birds/<string:bird_identifier>',
    'func': birds_rest_api.get_single_bird,
  },
  {
    'rule': '/birds/<string:bird_identifier>/statistics',
    'func': birds_rest_api.get_bird_statistics,
  },
  {
    'rule': '/birds/<string:bird_identifier>/common-names',
    'func': birds_rest_api.get_common_names,
  },
  {
    'rule': '/birds/<string:bird_identifier>/common-names/<int:id>',
    'func': birds_rest_api.get_common_name,
  },
  {
    'rule': '/birds/<string:bird_identifier>/common-names',
    'func': birds_rest_api.post_common_name,
    'options': {'methods': ['POST']},
  }
]

search_routes = [
  {
    'rule': '/search/birds',
    'func': search_api.search_birds,
  }
]

roles_routes = [
  {
    'rule': '/roles/<string:role_id>/permissions',
    'func': roles_rest_api.get_role_permissions,
  }
]

locales_routes = [
  {
    'rule': '/locales',
    'func': locales_rest_api.get_locales,
  }
]

registration_requests_routes = [
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

account_routes = [
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
    'rule': '/account/roles',
    'func': accounts_rest_api.get_authenticated_accounts_roles,
  },
  {
    'rule': '/account/password',
    'func': accounts_rest_api.post_password,
    'options': {'methods': ['POST']},
  },
]

authentication_routes = [
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

sightings_routes = [
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

birders_routes = [
  {
    'rule': '/birders',
    'func': birders_rest_api.get_birders,
  },
  {
    'rule': '/birders/<int:birder_id>',
    'func': birders_rest_api.get_birder,
  },
  {
    'rule': '/birders/<int:birder_id>/birder-connections',
    'func': birders_rest_api.get_birders_birder_connections,
  },
]
