from difflib import SequenceMatcher

from birding import LocaleRepository


class BirdSearchController:

  def __init__(self, bird_searcher):
    self.bird_searcher = bird_searcher

  def search(self, name):
    bird_matches = self.bird_searcher.search(name)
    bird_matches.sort(key=lambda m: m.query_match, reverse=True)
    return bird_matches[:100]

class BirdSearcher:

  def __init__(self, bird_repository, locale_repository: LocaleRepository, string_matcher):
    self.bird_repository = bird_repository
    self.locale_repository = locale_repository
    self.string_matcher = string_matcher

  def search(self, name=None):
    result_builder = ResultBuilder()
    birds = self.bird_repository.birds
    if name:
      binomial_name_matches = self.search_by_binomial_name(name)
      result_builder.add_matches(binomial_name_matches)
      language_name_matches = self.search_by_language_names(name)
      result_builder.add_matches(language_name_matches)
    return result_builder.create_bird_matches()

  def search_by_binomial_name(self, name):
    matches = dict()
    birds = self.bird_repository.birds
    for bird in birds:
      if name.lower() in bird.binomial_name.lower():
        matches[bird] = [self.string_matcher.match(name, bird.binomial_name)]
    return matches

  def search_by_language_names(self, name):
    matches = dict()
    birds = self.bird_repository.birds
    locales = [self.locale_repository.find_locale(x) for x in self.locale_repository.available_locale_codes()]
    dictionaries = [locale.bird_dictionary for locale in locales if locale.bird_dictionary]
    for dictionary in dictionaries:
      for bird in birds:
        binomial_name = bird.binomial_name
        if binomial_name in dictionary and name.lower() in dictionary[binomial_name].lower():
          match = self.string_matcher.match(name, dictionary[binomial_name])
          matches[bird] = matches[bird] + [match] if bird in matches else [match]
    return matches

class ResultBuilder:

  def __init__(self):
    self.matches_by_bird = dict()

  def add_matches(self, matches):
    if matches:
      for k, v in matches.items():
        for match in v:
          self.add_match(k, match)

  def add_match(self, bird, match):
    if bird not in self.matches_by_bird:
      self.matches_by_bird[bird] = []
    self.matches_by_bird[bird].append(match)

  def create_bird_matches(self):
    bird_matches = []
    for bird in self.matches_by_bird:
      query_match = self.__average_query_match(bird)
      bird_matches.append(BirdMatch(bird, query_match))
    return bird_matches

  def __average_query_match(self, bird):
    return sum(self.matches_by_bird[bird]) / len(self.matches_by_bird[bird])

class BirdMatch:

  def __init__(self, bird, query_match):
    self.__bird = bird
    self.__query_match = query_match

  @property
  def bird(self):
    return self.__bird

  @property
  def query_match(self):
    return self.__query_match

class StringMatcher:

  def match(self, a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()
