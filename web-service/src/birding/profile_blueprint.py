from flask import Blueprint
from flask import g

from birding.account import AccountRepository, Username
from birding.sighting import SightingRepository
from .render import render_page


def create_profile_blueprint(
      account_repository: AccountRepository,
      sighting_repository: SightingRepository):
  blueprint = Blueprint('profile', __name__)

  @blueprint.route('/profile/<username>')
  def get_profile(username):
    g.render_context['username'] = username
    profile_account = account_repository.find_user_account(Username(username))
    life_list_count = sighting_repository.get_life_list_count(profile_account)
    g.render_context['life_list_count'] = life_list_count
    return render_page('profile.html')

  return blueprint
