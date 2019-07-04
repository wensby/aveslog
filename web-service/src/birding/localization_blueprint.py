from flask import Blueprint, request, redirect, url_for, after_this_request, g


def update_locale_context(locale, user_locale_cookie_key):
  previously_set = request.cookies.get(user_locale_cookie_key, None)
  # when the response exists, set a cookie with the language if it is new
  if locale.language and (
        not previously_set or previously_set is not locale.language.iso_639_1_code):
    set_locale_cookie_after_this_request(locale, user_locale_cookie_key)
  g.locale = locale
  g.render_context['locale'] = locale


def set_locale_cookie_after_this_request(locale, user_locale_cookie_key):
  @after_this_request
  def remember_language(response):
    response.set_cookie(user_locale_cookie_key, locale.language.iso_639_1_code)
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
      update_locale_context(locale, user_locale_cookie_key)
      return redirect(url_for('home.index'))

  return blueprint
