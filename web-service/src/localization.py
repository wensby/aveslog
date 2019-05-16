import json

class LocalesFactory:

  def __init__(self, database, locales_directory_path):
    self.database = database
    self.locales_directory_path = locales_directory_path

  def create_locales(self):
    locales = dict()
    language_codes = self.__get_locale_codes()
    languages = map(lambda x: Language(x), language_codes)
    for language in languages:
      locales[language] = self.create_locale(language)
    return locales

  def __get_locale_codes(self):
    rows = self.database.query('SELECT code FROM locale;')
    if rows:
      return [row[0] for row in rows]

  def create_locale(self, language):
    language_dictionary = self.create_language_dictionary(language)
    bird_dictionary = self.create_bird_dictionary(language)
    return Locale(language, language_dictionary, bird_dictionary)

  def create_language_dictionary(self, language):
    lang_iso = language.iso_639_1_code
    dictionary_filepath = self.locales_directory_path + lang_iso + '.json'
    with open(dictionary_filepath, 'r') as file:
      return json.load(file)

  def create_bird_dictionary(self, language):
    bird_dictionary_factory = BirdDictionaryFactory(self.locales_directory_path)
    return bird_dictionary_factory.create_dictionary(language)

class Locale:

  def __init__(self, language, dictionary, bird_dictionary):
    self.language = language
    self.dictionary = dictionary
    self.bird_dictionary = bird_dictionary

  def text(self, text, variables=None):
    translated = self.dictionary[text] if text in self.dictionary else text
    if variables:
      i = 0
      while '{{}}' in translated:
        translated = translated.replace('{{}}', variables[i], 1)
        i = i + 1
    return translated

  def name(self, bird):
    if self.bird_dictionary and bird.binomial_name in self.bird_dictionary:
      return self.bird_dictionary[bird.binomial_name]

class BirdDictionaryFactory:

  def __init__(self, locales_directory_path):
    self.locales_directory_path = locales_directory_path

  def create_dictionary(self, language):
    filepath = self.locales_directory_path + 'bird-names-by-language.json'
    with open(filepath, 'r') as jsonfile:
      bird_names_by_language = json.load(jsonfile)
      if language.iso_639_1_code in bird_names_by_language:
        return bird_names_by_language[language.iso_639_1_code]

class Language:

  def __init__(self, iso_639_1_code):
    self.iso_639_1_code = iso_639_1_code

class LanguageRepository:

  def __init__(self, languages):
    self.languages = languages

class LanguageRepositoryFactory:

  def __init__(self, database):
    self.database = database

  def create_repository(self):
    languages = []
    self.database.query('SELECT ()')

class LocaleDeterminer:

  def __init__(self, locales, user_locale_cookie_key):
    self.locales = locales
    self.user_locale_cookie_key = user_locale_cookie_key

  def determine_locale_from_request(self, request):
    locale = self.__determine_from_cookies(request.cookies)
    if not locale:
      locale = self.__determine_from_headers(request.headers)
    if not locale:
      locale = self.locales[next(iter(self.locales))]
    return locale

  def __determine_from_cookies(self, cookies):
    cookie_locale_code = cookies.get(self.user_locale_cookie_key)
    if cookie_locale_code in self.__available_locale_codes():
      return self.__from_code(cookie_locale_code)

  def __determine_from_headers(self, headers):
    if 'Accept-Language' in headers:
      header = headers['Accept-Language']
      requested_codes = list(map(lambda c: c.split(';')[0], header.split(',')))
      available_codes = self.__available_locale_codes()
      matching_codes = filter(lambda c: c in available_codes, requested_codes)
      return self.__from_code(next(matching_codes, None))

  def __available_locale_codes(self):
    return list(map(lambda x: x.iso_639_1_code, self.locales.keys()))

  def __from_code(self, code):
    language = next(filter(lambda l: l.iso_639_1_code == code, self.locales), None)
    if language:
      return self.locales[language]
