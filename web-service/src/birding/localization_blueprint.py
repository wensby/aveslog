import os

from flask import Blueprint, request, redirect, url_for, after_this_request, g

from birding.localization import LocaleRepository, LoadedLocale, Locale, \
  LocaleLoader
from birding.account import AccountRepository

def update_locale_context(user_locale_cookie_key, loaded_locale: LoadedLocale):
  previously_set_code = request.cookies.get(user_locale_cookie_key, None)
  # when the response exists, set a cookie with the language if it is new
  if loaded_locale.locale.code and loaded_locale.locale.code is not previously_set_code:
    set_locale_cookie_after_this_request(loaded_locale.locale, user_locale_cookie_key)
  g.locale = loaded_locale
  g.render_context['locale'] = loaded_locale


def set_locale_cookie_after_this_request(locale: Locale, user_locale_cookie_key):
  @after_this_request
  def set_locale_cookie(response):
    response.set_cookie(user_locale_cookie_key, locale.code)
    return response


def create_localization_blueprint(locale_repository: LocaleRepository,
      locale_loader: LocaleLoader, user_locale_cookie_key: str,
      account_repository: AccountRepository):
  blueprint = Blueprint('localization', __name__)

  @blueprint.route('/language')
  def language():
    language_code = request.args.get('l')
    available_codes = locale_repository.available_locale_codes()
    if language_code in available_codes:
      locale = locale_repository.find_locale_by_code(language_code)
      if g.logged_in_account:
        account_repository.set_account_locale(g.logged_in_account.id, locale)
      if locale:
        loaded_locale = locale_loader.load_locale(locale)
        update_locale_context(user_locale_cookie_key, loaded_locale)
      return redirect(url_for('home.index'))

  return blueprint
