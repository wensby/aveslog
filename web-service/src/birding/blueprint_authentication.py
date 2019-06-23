from functools import wraps
import re
import os

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from .render import render_page
from .account import Credentials
from .authentication import AccountRegistrationRequest

def require_login(view):
  @wraps(view)
  def wrapped_view(**kwargs):
    if g.logged_in_account:
      return view(**kwargs)
    else:
      return redirect(url_for('authentication.get_login'))
  return wrapped_view

def require_logged_out(view):
  @wraps(view)
  def wrapped_view(**kwargs):
    if g.logged_in_account:
      return redirect(url_for('index'))
    else:
      return view(**kwargs)
  return wrapped_view

def create_authentication_blueprint(account_repository, person_repo, authenticator, account_registration_controller, password_reset_controller):
  blueprint = Blueprint('authentication', __name__, url_prefix='/authentication')
  
  @blueprint.before_app_request
  def load_logged_in_account():
    account_id = session.get('account_id')
    if account_id:
      g.logged_in_account = account_repository.get_user_account_by_id(account_id)
    else:
      g.logged_in_account = None

  @blueprint.route('/register/request')
  @require_logged_out
  def get_register_request():
    return render_page('registration_request.html')
  
  @blueprint.route('/password-reset')
  @require_logged_out
  def get_password_reset_request():
    return render_page('password_reset_request.html')

  @blueprint.route('/password-reset', methods=['POST'])
  @require_logged_out
  def post_password_reset_request():
    email = request.form['email']
    password_reset_controller.initiate_password_reset(email, g.locale)
    flash(g.locale.text(u"An email has been sent. If you have't received it in a few minutes, please check your spam folder."), 'success')
    return redirect(url_for('authentication.get_password_reset_request'))

  @blueprint.route('/password-reset/<token>')
  @require_logged_out
  def get_password_reset_form(token):
    g.render_context['password_reset_token'] = token
    return render_page('password_reset_form.html')

  @blueprint.route('/password-reset/<token>', methods=['POST'])
  @require_logged_out
  def post_password_reset_form(token):
    token = request.form['token']
    password = request.form['password']
    result = password_reset_controller.perform_password_reset(token, password)
    if result == 'success':
      flash(u"Your password has been reset.", 'success')
      return redirect(url_for('authentication.get_login'))
    else:
      flash(u"Something went wrong", 'danger')
      return redirect(url_for('authentication.get_password_reset_form', token=token))

  @blueprint.route('/register/request', methods=['POST'])
  @require_logged_out
  def post_register_request():
    email = request.form['email']
    locale = g.locale
    account_registration_controller.initiate_registration(email, locale)
    flash(g.locale.text(u'An email containing your registration form link has been sent to your email address.'), 'success')
    return redirect(url_for('authentication.get_register_request'))
  
  @blueprint.route('/register/form/<token>')
  @require_logged_out
  def get_register_form(token):
    registration = account_repository.find_account_registration_by_token(token)
    if registration:
      g.render_context['user_account_registration'] = registration
      return render_page('register.html')
    else:
      flash('This registration link is no longer valid, please request a new one.')
      return redirect(url_for('authentication.get_register_request'))
  
  @blueprint.route('/register/form/<token>', methods=['POST'])
  @require_logged_out
  def post_register_form(token):
    if not token == request.form['token']:
      flash(u'Account registraion failure: Registration token discrepancy', 'danger')
      return redirect(url_for('authentication.get_register_form', token=token))
    registration_request = AccountRegistrationRequest(
        request.form['email'],
        request.form['token'],
        request.form['username'],
        request.form['password']
    )
    response = account_registration_controller.perform_registration_request(registration_request)
    if response == 'success':
      flash(u'User account created succesfully', 'success')
      return redirect(url_for('authentication.get_login'))
    elif response == 'associated registration missing':
      flash(u'Registration form no longer valid', 'danger')
      return redirect(url_for('authentication.get_login'))
    elif response == 'username taken':
      flash(u'Username already taken', 'danger')
      return redirect(url_for('authentication.get_register_form', token=token))
    elif response == 'failure':
      flash(u'User account registration failed', 'danger')
      return redirect(url_for('authentication.get_register_form', token=token))
    else:
      flash(u'User account registration failed', 'danger')
      return redirect(url_for('authentication.get_register_form', token=token))

  @blueprint.route('/login')
  @require_logged_out
  def get_login():
    return render_page('login.html')
  
  @blueprint.route('/login', methods=['POST'])
  @require_logged_out
  def post_login():
    posted_username = request.form['username']
    posted_password = request.form['password']
    if Credentials.is_valid(posted_username, posted_password):
      credentials = Credentials(posted_username, posted_password)
      account = authenticator.get_authenticated_user_account(credentials)
      if account:
        session['account_id'] = account.id
        return redirect(url_for('index'))
    return redirect(url_for('authentication.get_login'))
  
  @blueprint.route('/logout')
  def logout():
    session.pop('account_id', None)
    return redirect(url_for('index'))

  return blueprint
