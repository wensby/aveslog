from flask import Blueprint

from birding.render import render_page


def create_home_blueprint():
  blueprint = Blueprint('home', __name__)

  @blueprint.route('/')
  def index():
    return render_page('index.html')

  return blueprint