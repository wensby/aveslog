from difflib import SequenceMatcher
from typing import Dict, List, Optional

from .bird import Bird
from .bird import BirdRepository
from .localization import LocaleRepository, LocaleLoader


class BirdMatch:

  def __init__(self, bird: Bird, query_match: float):
    self.bird = bird
    self.query_match = query_match


class StringMatcher:

  def match(self, a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


class BirdSearcher:

  def __init__(self,
        bird_repository: BirdRepository,
        locale_repository: LocaleRepository,
        string_matcher: StringMatcher,
        locale_loader: LocaleLoader,
  ):
    self.bird_repository = bird_repository
    self.locale_repository = locale_repository
    self.string_matcher = string_matcher
    self.locale_loader = locale_loader

  def search(self, name: Optional[str] = None) -> List[BirdMatch]:
    birds = self.bird_repository.birds
    result_builder = ResultBuilder(birds)
    if name:
      binomial_name_matches = self.search_by_binomial_name(birds, name)
      result_builder.add_matches(binomial_name_matches)
      language_name_matches = self.search_by_language_names(birds, name)
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

  def search_by_language_names(self,
        birds: List[Bird],
        name: str,
  ) -> Dict[Bird, List[float]]:
    matches = dict()
    for dictionary in self.__get_bird_dictionaries():
      for bird in birds:
        binomial_name = bird.binomial_name
        if binomial_name in dictionary and name.lower() in dictionary[
          binomial_name].lower():
          match = self.string_matcher.match(name, dictionary[binomial_name])
          matches[bird] = matches[bird] + [match] if bird in matches else [
            match]
    return matches

  def __get_bird_dictionaries(self):
    locales = self.locale_repository.locales
    loaded_locales = map(self.locale_loader.load_locale, locales)
    return [l.bird_dictionary for l in loaded_locales if l.bird_dictionary]


class BirdSearchController:

  def __init__(self, bird_searcher: BirdSearcher):
    self.bird_searcher = bird_searcher

  def search(self, name: str, limit: Optional[int]) -> List[BirdMatch]:
    bird_matches = self.bird_searcher.search(name)
    bird_matches.sort(key=lambda m: m.query_match, reverse=True)
    if limit:
      return bird_matches[:limit]
    else:
      return bird_matches[:20]


class ResultBuilder:

  def __init__(self, birds: List[Bird]):
    self.matches_by_bird: Dict[Bird, List[float]] = {bird: [] for bird in birds}

  def add_matches(self, matches: Dict[Bird, List[float]]):
    if matches:
      for k, v in matches.items():
        for match in v:
          self.add_match(k, match)

  def add_match(self, bird: Bird, match: float):
    self.matches_by_bird[bird].append(match)

  def create_bird_matches(self) -> List[BirdMatch]:
    bird_matches = []
    for bird in self.matches_by_bird:
      query_match = self.__average_query_match(bird)
      bird_matches.append(BirdMatch(bird, query_match))
    return bird_matches

  def __average_query_match(self, bird: Bird) -> float:
    if self.matches_by_bird[bird]:
      return sum(self.matches_by_bird[bird]) / len(self.matches_by_bird[bird])
    return 0.0
