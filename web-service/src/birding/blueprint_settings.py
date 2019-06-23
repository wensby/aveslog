from flask import Blueprint
from flask import session
from flask import g
from flask import request
from flask import flash
from .render import render_page
from .account import Credentials
from .account import is_valid_password
from .blueprint_authentication import require_login

def create_settings_blueprint(account_repository, authenticator, password_repository):
  blueprint = Blueprint('settings', __name__, url_prefix='/settings')

  @blueprint.route('/')
  @require_login
  def get_settings_index():
    g.render_context['username'] = g.logged_in_account.username
    return render_page('settings/index.html')

  @blueprint.route('/password')
  @require_login
  def get_password_settings():
    g.render_context['username'] = g.logged_in_account.username
    return render_page('settings/password.html')

  @blueprint.route('/password', methods=['POST'])
  @require_login
  def post_password_settings():
    account = g.logged_in_account
    username = account.username
    g.render_context['username'] = username
    oldpassword = request.form['oldPasswordInput']
    if is_password_change_valid(account, request.form):
      newpassword = request.form['newPasswordInput']
      password_repository.update_password(account.id, newpassword)
      flash('success')
    else:
      flash('failure')
    return render_page('settings/password.html')

  def is_password_change_valid(account, form):
    oldpassword = request.form['oldPasswordInput']
    if authenticator.is_account_password_correct(account, oldpassword):
      return is_posted_new_password_valid(form)

  def is_posted_new_password_valid(form):
    newpassword = form['newPasswordInput']
    newpasswordverification = form['newPasswordVerificationInput']
    return newpassword == newpasswordverification and is_valid_password(newpassword)

  return blueprint

