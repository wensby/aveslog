import json

class Language:

  def __init__(self, iso_639_1_code):
    self.iso_639_1_code = iso_639_1_code

  def bird_names(self):
    with open('locales/bird-names-by-language.json', 'r') as jsonfile:
      names_by_language = json.load(jsonfile)
      if self.iso_639_1_code in names_by_language:
        return names_by_language[self.iso_639_1_code]

class LanguageRepository:

  def __init__(self, languages):
    self.languages = languages

class LanguageRepositoryFactory:

  def __init__(self, database):
    self.database = database

  def create_repository(self):
    languages = []
    self.database.query('SELECT ()')

class Locale:

  def __init__(self, id, dictionary, bird_names):
    self.id = id
    self.dictionary = dictionary
    self.bird_names = bird_names

  def text(self, text, variables=None):
    translated = self.dictionary[text] if text in self.dictionary else text
    if variables:
      i = 0
      while '{{}}' in translated:
        translated = translated.replace('{{}}', variables[i], 1)
        i = i + 1
    return translated

  def name(self, bird):
    if bird.binomial_name in self.bird_names:
      return self.bird_names[bird.binomial_name]

class LocaleRepository:

  def __init__(self, locale_dictionary_path):
    self.locales = dict()
    self.languages = [Language('sv'), Language('en'), Language('ko')]
    for lang in self.languages:
      iso_lang = lang.iso_639_1_code
      with open(locale_dictionary_path + iso_lang + '.json', 'r') as f:
        dictionary = json.load(f)
        self.locales[iso_lang] = Locale(iso_lang, dictionary, None)

  def get_locale(self, language):
    return self.locales[language]

class LocaleDeterminer:

  def __init__(self, locale_repository):
    self.repository = locale_repository

  def figure_out_language_from_request_cookies(self, cookies):
    user_lang = cookies.get('user_lang')
    if user_lang in map(lambda x: x.iso_639_1_code, self.repository.languages):
      return user_lang

  def figure_out_language_from_request_headers(self, headers):
    supported = map(lambda x: x.iso_639_1_code, self.repository.languages)
    if 'Accept-Language' in headers:
      requested = headers['Accept-Language'].split(',')
      matches = filter(lambda x: x.split(';')[0] in supported, requested)
      return next(matches, next(iter(supported))).split(';')[0]
    return next(iter(supported))

  def figure_out_language_from_request(self, request):
    language = self.figure_out_language_from_request_cookies(request.cookies)
    if language is None:
      language = self.figure_out_language_from_request_headers(request.headers)
    return language
