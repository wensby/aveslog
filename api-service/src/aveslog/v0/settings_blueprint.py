from flask import after_this_request
from flask import g
from flask import request

from aveslog.v0.localization import LoadedLocale
from aveslog import Locale


def update_locale_context(user_locale_cookie_key, loaded_locale: LoadedLocale):
  previously_set_code = request.cookies.get(user_locale_cookie_key, None)
  # when the response exists, set a cookie with the language if it is new
  if loaded_locale.locale.code and loaded_locale.locale.code is not previously_set_code:
    set_locale_cookie_after_this_request(loaded_locale.locale,
                                         user_locale_cookie_key)
  g.locale = loaded_locale


def set_locale_cookie_after_this_request(locale: Locale,
      user_locale_cookie_key):
  @after_this_request
  def set_locale_cookie(response):
    response.set_cookie(user_locale_cookie_key, locale.code)
    return response
