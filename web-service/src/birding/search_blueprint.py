from flask import Blueprint
from flask import request
from flask import g
from .render import render_page

def create_search_blueprint(bird_search_controller, bird_search_view_factory):
  controller = bird_search_controller
  view_factory = bird_search_view_factory

  blueprint = Blueprint('search', __name__)


  
  return blueprint
