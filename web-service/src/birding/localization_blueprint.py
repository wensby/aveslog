from flask import Blueprint, request, redirect, url_for, after_this_request, g


def update_locale_context(user_locale_cookie_key, locale):
  previously_set_code = request.cookies.get(user_locale_cookie_key, None)
  # when the response exists, set a cookie with the language if it is new
  if locale.code and locale.code is not previously_set_code:
    set_locale_cookie_after_this_request(locale, user_locale_cookie_key)
  g.locale = locale
  g.render_context['locale'] = locale


def set_locale_cookie_after_this_request(locale, user_locale_cookie_key):
  @after_this_request
  def set_locale_cookie(response):
    response.set_cookie(user_locale_cookie_key, locale.code)
    return response


def create_localization_blueprint(locale_repository, locale_loader,
      user_locale_cookie_key):
  blueprint = Blueprint('localization', __name__)

  @blueprint.route('/language')
  def language():
    language_code = request.args.get('l')
    available_codes = locale_repository.available_locale_codes()
    if language_code in available_codes:
      locale = locale_loader.load_locale(language_code)
      update_locale_context(user_locale_cookie_key, locale)
      return redirect(url_for('home.index'))

  return blueprint
