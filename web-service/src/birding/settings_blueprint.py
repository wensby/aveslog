from flask import Blueprint, after_this_request
from flask import g
from flask import request
from flask import flash
from flask import redirect
from flask import url_for

from birding.localization import LoadedLocale, Locale, LocaleRepository, \
  LocaleLoader
from .render import render_page
from .account import Password, AccountRepository
from .authentication_blueprint import require_login

def update_locale_context(user_locale_cookie_key, loaded_locale: LoadedLocale):
  previously_set_code = request.cookies.get(user_locale_cookie_key, None)
  # when the response exists, set a cookie with the language if it is new
  if loaded_locale.locale.code and loaded_locale.locale.code is not previously_set_code:
    set_locale_cookie_after_this_request(loaded_locale.locale,
                                         user_locale_cookie_key)
  g.locale = loaded_locale
  g.render_context['locale'] = loaded_locale

def set_locale_cookie_after_this_request(locale: Locale,
      user_locale_cookie_key):
  @after_this_request
  def set_locale_cookie(response):
    response.set_cookie(user_locale_cookie_key, locale.code)
    return response

def create_settings_blueprint(authenticator, password_repository,
      locale_repository: LocaleRepository,
      account_repository: AccountRepository,
      locale_loader: LocaleLoader,
      user_locale_cookie_key: str):
  blueprint = Blueprint('settings', __name__, url_prefix='/settings')

  @blueprint.route('/')
  def get_settings_index():
    return render_page('settings/index.html')

  @blueprint.route('/language/<l>')
  def language(l):
    language_code = l
    available_codes = locale_repository.available_locale_codes()
    if language_code in available_codes:
      locale = locale_repository.find_locale_by_code(language_code)
      if g.logged_in_account:
        account_repository.set_account_locale(g.logged_in_account.id, locale)
      if locale:
        loaded_locale = locale_loader.load_locale(locale)
        update_locale_context(user_locale_cookie_key, loaded_locale)
    return redirect(url_for('settings.get_settings_index'))

  @blueprint.route('/password')
  @require_login
  def get_password_settings():
    g.render_context['username'] = g.logged_in_account.username
    return render_page('settings/password.html')

  @blueprint.route('/password', methods=['POST'])
  @require_login
  def post_password_settings():
    old_password = request.form['oldPasswordInput']
    new_password = request.form['newPasswordInput']
    account = g.logged_in_account
    if is_password_change_valid(account, old_password, new_password):
      password_repository.update_password(account.id, Password(new_password))
      flash('success')
    else:
      flash('failure')
    return render_page('settings/password.html')

  def is_password_change_valid(account, old_password, new_password):
    if Password.is_valid(old_password) and Password.is_valid(new_password):
      return authenticator.is_account_password_correct(
        account, Password(old_password))

  return blueprint
