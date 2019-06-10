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
from .user_account import Credentials
from .mail import EmailAddress

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

def create_authentication_blueprint(account_repository, mail_dispatcher, person_repo, authenticator, account_registration_controller):
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
  
  @blueprint.route('/register/request', methods=['POST'])
  @require_logged_out
  def post_register_request():
    email = request.form['email']
    account_registration_controller.prepare_account_registration(email)
    flash(g.locale.text(u'An email containing your registration form link has been sent to your email address.'), 'success')
    return redirect(url_for('authentication.get_register_request'))
  
  @blueprint.route('/register/form/<token>')
  @require_logged_out
  def get_register_form(token):
    registration = account_repository.get_user_account_registration_by_token(token)
    if registration:
      g.render_context['user_account_registration'] = registration
      return render_page('register.html')
    else:
      flash('This registration link is no longer valid, please request a new one.')
      return redirect(url_for('authentication.get_register_request'))
  
  @blueprint.route('/register/form/<token>', methods=['POST'])
  @require_logged_out
  def post_register_form(token):
    formemail = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    formtoken = request.form['token']
    registration = account_repository.get_user_account_registration_by_token(token)
    if formtoken == token and formemail == registration.email and password == confirmPassword:
      # if username already present
      if account_repository.find_user_account(username):
        flash('username already taken')
        return redirect(url_for('authentication.get_register_form', token=token))
      else:
        account = account_repository.put_new_user_account(formemail, username, password)
        if account:
          # account created, remove the registration token
          account_repository.remove_user_account_registration_by_id(registration.id)
          person = person_repo.add_person(username)
          account_repository.set_user_account_person(account, person)
          flash(u'user account created', 'success')
          return redirect(url_for('authentication.get_login'))
    flash(u'user account creation failed', 'danger')
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
