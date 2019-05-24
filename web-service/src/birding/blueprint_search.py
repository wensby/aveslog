from flask import Blueprint
from flask import request
from flask import g
from flask import session
from .render import render_page

def create_search_blueprint(bird_searcher, account_repo):
  blueprint = Blueprint('search', __name__)

  @blueprint.route('/bird/search')
  def bird_search():
    name = request.args.get('query')
    bird_matches = bird_searcher.search(name)
    g.render_context['bird_matches'] = list(bird_matches)
    if 'account_id' in session:
      account = account_repo.get_user_account_by_id(session['account_id'])
      g.render_context['username'] = account.username
    return render_page('birdsearch.html')
  
  return blueprint
