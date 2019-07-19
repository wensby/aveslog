from flask import Blueprint
from flask import g
from flask import request
from flask import flash
from .render import render_page
from .account import Password
from .authentication_blueprint import require_login


def create_settings_blueprint(authenticator, password_repository):
  blueprint = Blueprint('settings', __name__, url_prefix='/settings')

  @blueprint.route('/')
  def get_settings_index():
    return render_page('settings/index.html')

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
