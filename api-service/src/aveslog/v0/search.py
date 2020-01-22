from difflib import SequenceMatcher
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from .models import Bird
from .models import BirdName


class BirdSearchMatch:

  def __init__(self, bird: Bird, score: float):
    self.bird = bird
    self.score = score


class StringMatcher:

  def match(self, a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


class BirdSearcher:

  def __init__(self, session: Session, string_matcher: StringMatcher):
    self.session = session
    self.string_matcher = string_matcher

  def search(self, name: Optional[str] = None) -> List[BirdSearchMatch]:
    birds = self.session.query(Bird).all()
    scores_by_bird: Dict[Bird, List[float]] = {}
    if name:
      binomial_name_matches = self.search_by_binomial_name(birds, name)
      for bird in binomial_name_matches:
        if bird not in scores_by_bird:
          scores_by_bird[bird] = []
        scores_by_bird[bird].append(binomial_name_matches[bird][0])
      language_name_matches = self.search_by_language_names(name)
      for bird in language_name_matches:
        if bird not in scores_by_bird:
          scores_by_bird[bird] = []
        scores_by_bird[bird].append(language_name_matches[bird][0])
    matches = []
    for bird in scores_by_bird:
      score = sum(scores_by_bird[bird]) / len(scores_by_bird[bird])
      matches.append(BirdSearchMatch(bird, score))
    return matches

  def search_by_binomial_name(self,
        birds: List[Bird],
        name: str,
  ) -> Dict[Bird, List[float]]:
    matches = dict()
    for bird in birds:
      if name.lower() in bird.binomial_name.lower():
        matches[bird] = [self.string_matcher.match(name, bird.binomial_name)]
    return matches

  def search_by_language_names(self, name: str) -> Dict[Bird, List[float]]:
    matches = dict()
    bird_names: List[BirdName] = self.session.query(BirdName) \
      .filter(BirdName.name.ilike(f'%{name}%')) \
      .all()
    for bird_name in bird_names:
      bird = bird_name.bird
      match = self.string_matcher.match(name.lower(), bird_name.name.lower())
      matches[bird] = matches[bird] + [match] if bird in matches else [match]
    return matches
