from flask import Blueprint
from flask import session
from flask import g
from flask import request
from flask import flash
from .render import render_page
from .user_account import Credentials
from .user_account import is_valid_password

def create_settings_blueprint(account_repository, authenticator):
  blueprint = Blueprint('settings', __name__, url_prefix='/settings')

  @blueprint.route('/')
  def get_settings_index():
    if 'account_id' in session:
      account = account_repository.get_user_account_by_id(session['account_id'])
      g.render_context['username'] = account.username
      return render_page('settings/index.html')
    else:
      return redirect(url_for('sighting.index'))

  @blueprint.route('/password')
  def get_password_settings():
    if 'account_id' in session:
      account = account_repository.get_user_account_by_id(session['account_id'])
      g.render_context['username'] = account.username
      return render_page('settings/password.html')
    else:
      return redirect(url_for('sighting.index'))

  @blueprint.route('/password', methods=['POST'])
  def post_password_settings():
    if 'account_id' in session:
      account = account_repository.get_user_account_by_id(session['account_id'])
      username = account.username
      g.render_context['username'] = username
      oldpassword = request.form['oldPasswordInput']
      if is_password_change_valid(account, request.form):
        newpassword = request.form['newPasswordInput']
        account_repository.update_password(account, newpassword)
        flash('success')
      else:
        flash('failure')
      return render_page('settings/password.html')
    else:
      return redirect(url_for('sighting.index'))

  def is_password_change_valid(account, form):
    oldpassword = request.form['oldPasswordInput']
    if authenticator.is_account_password_correct(account, oldpassword):
      return is_posted_new_password_valid(form)

  def is_posted_new_password_valid(form):
    newpassword = form['newPasswordInput']
    newpasswordverification = form['newPasswordVerificationInput']
    return newpassword == newpasswordverification and is_valid_password(newpassword)

  return blueprint

