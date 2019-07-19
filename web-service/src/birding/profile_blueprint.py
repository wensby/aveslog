from flask import Blueprint
from flask import g
from .render import render_page


def create_profile_blueprint():
  blueprint = Blueprint('profile', __name__)

  @blueprint.route('/profile/<username>')
  def get_profile(username):
    g.render_context['username'] = username
    return render_page('profile.html')

  return blueprint
