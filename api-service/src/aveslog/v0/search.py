from typing import Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from .models import Bird
from .models import BirdCommonName


class BirdSearchMatch:

  def __init__(self, bird: Bird, score: float):
    self.bird = bird
    self.score = score


class BirdSearcher:

  def __init__(self, session: Session):
    self.session = session

  def search(self, name: Optional[str] = None) -> List[BirdSearchMatch]:
    scores_by_bird: Dict[Bird, List[float]] = {}
    if name:
      binomial_name_matches = self.search_by_binomial_name(name)
      for bird in binomial_name_matches:
        if bird not in scores_by_bird:
          scores_by_bird[bird] = []
        scores_by_bird[bird].append(binomial_name_matches[bird][0])
      language_name_matches = self.search_by_language_names(name)
      for bird in language_name_matches:
        if bird not in scores_by_bird:
          scores_by_bird[bird] = []
        scores_by_bird[bird].extend(language_name_matches[bird])
    matches = []
    for bird in scores_by_bird:
      score = max(scores_by_bird[bird])
      matches.append(BirdSearchMatch(bird, score))
    return matches

  def search_by_binomial_name(self, name: str) -> Dict[Bird, List[float]]:
    result = self.session.query(Bird, func.similarity(Bird.binomial_name, name)) \
      .filter(func.similarity(Bird.binomial_name, name) > 0.3) \
      .all()
    matches = dict()
    for bird, similarity in result:
      matches[bird] = [similarity]
    return matches

  def search_by_language_names(self, name: str) -> Dict[Bird, List[float]]:
    result = self.session.query(BirdCommonName, func.similarity(BirdCommonName.name, name)) \
      .filter(func.similarity(BirdCommonName.name, name) > 0.3) \
      .all()
    matches = dict()
    for common_name, similarity in result:
      bird = common_name.bird
      match = similarity
      matches[bird] = matches[bird] + [match] if bird in matches else [match]
    return matches
