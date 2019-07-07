from functools import wraps
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from .render import render_page
from .account import Credentials
from .account import Username
from .account import Password

def require_login(view):
  @wraps(view)
  def wrapped_view(**kwargs):
    if g.logged_in_account:
      return view(**kwargs)
    else:
      return redirect(url_for('authentication.get_login'))
  return wrapped_view

def require_logout(view):
  @wraps(view)
  def wrapped_view(**kwargs):
    if g.logged_in_account:
      return redirect(url_for('home.index'))
    else:
      return view(**kwargs)
  return wrapped_view

def create_authentication_blueprint(account_repository, authenticator, account_registration_controller, password_reset_controller):
  blueprint = Blueprint('authentication', __name__, url_prefix='/authentication')

  @blueprint.route('/register')
  @require_logout
  def get_register_request():
    return render_page('registration_request.html')
  
  @blueprint.route('/register', methods=['POST'])
  @require_logout
  def post_register_request():
    email = request.form['email']
    result = account_registration_controller.initiate_registration(email, g.locale)
    flash(g.locale.text(u'An email containing your registration form link has been sent to your email address.'), 'success')
    return redirect(url_for('authentication.get_register_request'))
  
  @blueprint.route('/register/<token>')
  @require_logout
  def get_register_form(token):
    registration = account_repository.find_account_registration_by_token(token)
    if registration:
      g.render_context['user_account_registration'] = registration
      return render_page('register.html')
    else:
      flash(g.locale.text('This registration link is no longer valid, please request a new one.'))
      return redirect(url_for('authentication.get_register_request'))
  
  @blueprint.route('/register/<token>', methods=['POST'])
  @require_logout
  def post_register_form(token):
    if not token == request.form['token']:
      flash(g.locale.text('Account registraion failure: Registration token discrepancy'), 'danger')
      return redirect(url_for('authentication.get_register_form', token=token))
    response = account_registration_controller.perform_registration(
        request.form['email'],
        request.form['token'],
        request.form['username'],
        request.form['password']
    )
    if response == 'associated registration missing':
      flash(g.locale.text('Registration form no longer valid'), 'danger')
      return redirect(url_for('authentication.get_login'))
    elif response == 'username taken':
      flash(g.locale.text('Username already taken'), 'danger')
      return redirect(url_for('authentication.get_register_form', token=token))
    assert response == 'success'
    flash(g.locale.text('User account created successfully'), 'success')
    return redirect(url_for('authentication.get_login'))

  @blueprint.route('/password-reset')
  @require_logout
  def get_password_reset_link_request():
    return render_page('password_reset_link_request.html')

  @blueprint.route('/password-reset', methods=['POST'])
  @require_logout
  def post_password_reset_request():
    email = request.form['email']
    password_reset_controller.initiate_password_reset(email, g.locale)
    flash(g.locale.text(u"An email has been sent. If you have't received it in a few minutes, please check your spam folder."), 'success')
    return redirect(url_for('authentication.get_password_reset_link_request'))

  @blueprint.route('/password-reset/<token>')
  @require_logout
  def get_password_reset_form(token):
    g.render_context['password_reset_token'] = token
    return render_page('password_reset_form.html')

  @blueprint.route('/password-reset/<token>', methods=['POST'])
  @require_logout
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


  @blueprint.route('/login')
  @require_logout
  def get_login():
    return render_page('login.html')
  
  @blueprint.route('/login', methods=['POST'])
  @require_logout
  def post_login():
    posted_username = request.form['username']
    posted_password = request.form['password']
    if Username.is_valid(posted_username) and Password.is_valid(posted_password):
      username = Username(posted_username)
      password = Password(posted_password)
      credentials = Credentials(username, password)
      account = authenticator.get_authenticated_user_account(credentials)
      if account:
        session['account_id'] = account.id
        return redirect(url_for('home.index'))
    return redirect(url_for('authentication.get_login'))
  
  @blueprint.route('/logout')
  def logout():
    session.pop('account_id', None)
    return redirect(url_for('home.index'))

  return blueprint
