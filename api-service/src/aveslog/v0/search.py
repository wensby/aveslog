import re
from typing import Dict, List, Optional

from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session
from sqlalchemy import func
import shlex

from .models import Bird
from .models import BirdCommonName
from .models import Sighting
from .models import Position


class BirdSearchMatch:

  def __init__(self, bird: Bird, score: float):
    self.bird = bird
    self.score = score

qualifiers = ['position']


class BirdSearcher:

  def __init__(self, session: Session):
    self.session = session

  def search(self, query: Optional[str] = None) -> List[BirdSearchMatch]:
    parts = shlex.split(query)
    scores_by_bird: Dict[Bird, float] = {}
    name_query = ' '.join([x for x in parts if x.split(':')[0] not in qualifiers])
    if name_query:
      name_search_scores = self.name_search(name_query)
      scores_by_bird = name_search_scores
    position_qualifiers = [x for x in parts if x.startswith('position:')]
    sighting_search_scores = {}
    if position_qualifiers:
      sighting_search_scores = self.search_by_sightings(position_qualifiers[-1])
    if not scores_by_bird:
      scores_by_bird = sighting_search_scores
    elif sighting_search_scores:
      for bird in scores_by_bird:
        sighting_score = sighting_search_scores.get(bird, 0)
        scores_by_bird[bird] = scores_by_bird[bird] * sighting_score
    matches = []
    for bird in scores_by_bird:
      matches.append(BirdSearchMatch(bird, scores_by_bird[bird]))
    return matches

  def name_search(self, name_query):
    scores_by_bird: Dict[Bird, float] = dict()
    binomial_name_matches = self.search_by_binomial_name(name_query)
    for bird in binomial_name_matches:
      scores_by_bird[bird] = binomial_name_matches[bird]
    language_name_matches = self.search_by_language_names(name_query)
    for bird in language_name_matches:
      scores_by_bird[bird] = max(scores_by_bird.get(bird, 0), language_name_matches[bird])
    return scores_by_bird

  def search_by_binomial_name(self, name: str) -> Dict[Bird, float]:
    result = self.session.query(Bird, func.similarity(Bird.binomial_name, name)) \
      .filter(func.similarity(Bird.binomial_name, name) > 0.3) \
      .all()
    matches = dict()
    for bird, similarity in result:
      matches[bird] = similarity
    return matches

  def search_by_language_names(self, name: str) -> Dict[Bird, float]:
    result = self.session.query(BirdCommonName, func.similarity(BirdCommonName.name, name)) \
      .filter(func.similarity(BirdCommonName.name, name) > 0.3) \
      .all()
    matches = dict()
    for common_name, similarity in result:
      bird = common_name.bird
      matches[bird] = max(matches.get(bird, 0), similarity)
    return matches

  def search_by_sightings(self, position_query: str) -> Dict[Bird, float]:
    matches = dict()
    match = re.match('position:([0-9.]+),([0-9.]+);r=([0-9.]+)', position_query)
    if match:
      lat = match.group(1)
      lon = match.group(2)
      radius = float(match.group(3))
      result = self.session.query(Bird, func.count(Sighting.bird)) \
        .join(Sighting.bird) \
        .join(Sighting.position) \
        .filter(func.ST_DistanceSphere(func.ST_GeomFromText(func.ST_AsText(Position.point), 4326), func.ST_GeomFromText(f'POINT({lon} {lat})', 4326)) < 1000 * radius) \
        .group_by(Bird) \
        .all()
      total = sum([count for _, count in result])
      for bird, count in result:
        score = count / total
        matches[bird] = score
    return matches

def create_position(lat, lon):
  element = WKTElement(f'POINT({lon} {lat})')
  return Position(point=element)