from flask import Blueprint
from flask import session
from flask import g
from .render import render_page
from .blueprint_authentication import require_login

def create_profile_blueprint(account_repo):
  blueprint = Blueprint('profile', __name__)

  @blueprint.route('/profile')
  @require_login
  def get_profile():
    g.render_context['username'] = g.logged_in_account.username
    return render_page('profile.html')

  return blueprint
