from difflib import SequenceMatcher
from typing import Dict, List, Optional

from flask import g
from sqlalchemy.orm import Session

from .models import Bird, BirdName
from .localization import LocaleRepository, LocaleLoader


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
    result_builder = ResultBuilder(birds)
    if name:
      binomial_name_matches = self.search_by_binomial_name(birds, name)
      result_builder.add_matches(binomial_name_matches)
      language_name_matches = self.search_by_language_names(name)
      result_builder.add_matches(language_name_matches)
    return result_builder.create_bird_matches()

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


class ResultBuilder:

  def __init__(self, birds: List[Bird]):
    self.matches_by_bird: Dict[Bird, List[float]] = {bird: [] for bird in birds}

  def add_matches(self, matches: Dict[Bird, List[float]]):
    if matches:
      for bird, scores in matches.items():
        for score in scores:
          self.add_match_score(bird, score)

  def add_match_score(self, bird: Bird, score: float):
    self.matches_by_bird[bird].append(score)

  def create_bird_matches(self) -> List[BirdSearchMatch]:
    matches = []
    for bird in self.matches_by_bird:
      score = self.__average_score(bird)
      if score > 0:
        matches.append(BirdSearchMatch(bird, score))
    return matches

  def __average_score(self, bird: Bird) -> float:
    if self.matches_by_bird[bird]:
      return sum(self.matches_by_bird[bird]) / len(self.matches_by_bird[bird])
    return 0.0
