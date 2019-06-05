class BirdSearcher:

  def __init__(self, bird_repository, locales):
    self.bird_repository = bird_repository
    self.locales = locales

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
        matches[bird] = Match()
    return matches

  def search_by_language_names(self, name):
    matches = dict()
    birds = self.bird_repository.birds
    locales = self.locales
    dictionaries = [v.bird_dictionary for k, v in locales.items() if v.bird_dictionary]
    for dictionary in dictionaries:
      for bird in birds:
        binomial_name = bird.binomial_name
        if binomial_name in dictionary and name.lower() in dictionary[binomial_name].lower():
          match = Match()
          matches[bird] = matches[bird] + [match] if bird in matches else [match]
    return matches

class ResultBuilder:

  def __init__(self):
    self.matches_by_bird = dict()

  def add_matches(self, matches):
    if matches:
      for k, v in matches.items():
        self.add_match(k, v)

  def add_match(self, bird, match):
    if bird not in self.matches_by_bird:
      self.matches_by_bird[bird] = []
    self.matches_by_bird[bird].append(match)

  def create_bird_matches(self):
    bird_matches = []
    for bird in self.matches_by_bird:
      bird_matches.append(BirdMatch(bird, 1))
    return bird_matches

class Match:

  def __init__(self):
    pass

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
