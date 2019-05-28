from flask import Blueprint
from flask import session
from flask import g
from .render import render_page

def create_profile_blueprint(account_repo):
  blueprint = Blueprint('profile', __name__)

  @blueprint.route('/profile')
  def get_profile():
    if 'account_id' in session:
      account = account_repo.get_user_account_by_id(session['account_id'])
      g.render_context['username'] = account.username
      return render_page('profile.html')
    else:
      return render_page('index.html')

  return blueprint
