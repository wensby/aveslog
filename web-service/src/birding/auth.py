import functools
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

def create_auth_blueprint(account_repo, mail_dispatcher, person_repo, authenticator):
  blueprint = Blueprint('auth', __name__)
  
  @blueprint.route('/registration_request')
  def get_registration_request():
    return render_page('registration_request.html')
  
  @blueprint.route('/registration_request', methods=['POST'])
  def post_registration_request():
    email = request.form['email']
    email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if email_pattern.match(email):
      account_repo.put_user_account_registration(email)
      registration = account_repo.get_user_account_registration_by_email(email)
      token = registration.token
      link = os.environ['HOST'] + url_for('auth.get_register_token', token=token)
      mail_dispatcher.dispatch(email, 'Birding Registration', 'Link: ' + link)
    flash('Please check your email inbox for your registration link.')
    return redirect(url_for('auth.get_registration_request'))
  
  @blueprint.route('/register/<token>')
  def get_register_token(token):
    registration = account_repo.get_user_account_registration_by_token(token)
    if registration:
      g.render_context['user_account_registration'] = registration
      return render_page('register.html')
    else:
      flash('This registration link is no longer valid, please request a new one.')
      return redirect(url_for('auth.get_registration_request'))
  
  @blueprint.route('/register/<token>', methods=['POST'])
  def post_register_token(token):
    formemail = request.form['email']
    username = request.form['username']
    password = request.form['password']
    formtoken = request.form['token']
    registration = account_repo.get_user_account_registration_by_token(token)
    if formtoken == token and formemail == registration.email:
      # if username already present
      if account_repo.find_user_account(username):
        flash('username already taken')
        return redirect(url_for('auth.get_register_token', token=token))
      else:
        account = account_repo.put_new_user_account(formemail, username, password)
        if account:
          # account created, remove the registration token
          account_repo.remove_user_account_registration_by_id(registration.id)
          person = person_repo.add_person(username)
          account_repo.set_user_account_person(account, person)
          flash('user account created')
          return redirect(url_for('auth.get_login'))
    flash('user account creation failed')
    return redirect(url_for('auth.get_register_token', token=token))
  
  @blueprint.route('/login', methods=['POST'])
  def post_login():
    posted_username = request.form['username']
    posted_password = request.form['password']
    if Credentials.is_valid(posted_username, posted_password):
      credentials = Credentials(posted_username, posted_password)
      account = authenticator.get_authenticated_user_account(credentials)
      if account:
        session['account_id'] = account.id
        return redirect(url_for('sighting.index'))
    return redirect(url_for('auth.get_login'))
  
  @blueprint.route('/login', methods=['GET'])
  def get_login():
    return render_page('login.html')
  
  @blueprint.route('/logout', methods=['GET'])
  def logout():
    session.pop('account_id', None)
    return redirect(url_for('sighting.index'))

  return blueprint
