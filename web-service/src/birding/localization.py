import json
import os

from birding.database import Database
from .bird import Bird

class LocaleLoader:

  def __init__(self, locales_directory_path):
    self.locales_directory_path = locales_directory_path

  def load_locale(self, lang_iso):
    language_dictionary = None
    bird_dictionary = None
    dictionary_filepath = (
        f'{self.locales_directory_path}{lang_iso}/{lang_iso}.json')
    if os.path.exists(dictionary_filepath):
      with open(dictionary_filepath, 'r') as file:
        language_dictionary = json.load(file)
    language = Language(lang_iso)
    bird_dictionary_filepath = (
        f'{self.locales_directory_path}/{lang_iso}/{lang_iso}-bird-names.json')
    if os.path.exists(bird_dictionary_filepath):
      with open(bird_dictionary_filepath, 'r') as file:
        bird_dictionary = json.load(file)
    return Locale(language, language_dictionary, bird_dictionary)

class LocaleRepository:

  def __init__(self, locales_directory_path, locale_loader: LocaleLoader, database: Database):
    self.locales_directory_path = locales_directory_path
    self.locale_loader = locale_loader
    self.database = database

  def available_locale_codes(self):
    def is_length_2(x):
      return len(x) == 2
    def locales_directory_subdirectories():
      path = self.locales_directory_path
      return filter(lambda x: os.path.isdir(path + x), os.listdir(path))
    return list(filter(is_length_2, locales_directory_subdirectories()))

  def enabled_locale_codes(self):
    with self.database.transaction() as transaction:
      result = transaction.execute('SELECT id, code FROM locale;')
      return list(map(lambda x: x[0], result.rows))

  def find_locale_by_id(self, id):
    with self.database.transaction() as transaction:
      result = transaction.execute('SELECT code FROM locale WHERE id = %s;', (id, ))
      return self.find_locale(result.rows[0][0])

  def find_locale(self, code):
    return self.locale_loader.load_locale(code)

class LocalesFactory:

  def __init__(self, database, locales_directory_path):
    self.database = database
    self.locales_directory_path = locales_directory_path

  def create_locales(self):
    locales = dict()
    language_codes = self.__get_locale_codes()
    if language_codes:
      languages = map(lambda x: Language(x), language_codes)
      for language in languages:
          locales[language] = self.create_locale(language)
    return locales

  def __get_locale_codes(self):
    rows = self.database.query('SELECT code FROM locale;').rows
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
    if self.dictionary:
      translated = self.dictionary[text] if text in self.dictionary else text
    else:
      translated = text
    if variables:
      i = 0
      while '{{}}' in translated:
        translated = translated.replace('{{}}', variables[i], 1)
        i = i + 1
    return translated

  def name(self, bird):
    binomial_name = bird.binomial_name if isinstance(bird, Bird) else bird
    if self.bird_dictionary and binomial_name in self.bird_dictionary:
      return self.bird_dictionary[binomial_name]

class BirdDictionaryFactory:

  def __init__(self, locales_directory_path):
    self.locales_directory_path = locales_directory_path

  def create_dictionary(self, language):
    filepath = self.locales_directory_path + 'bird-names-by-language.json'
    with open(filepath, 'r') as jsonfile:
      bird_names_by_language = json.load(jsonfile)
      if language.iso_639_1_code in bird_names_by_language:
        return bird_names_by_language[language.iso_639_1_code]
    bird_name_filename = 'bird-names-' + language.iso_639_1_code + '.json'
    bird_name_filepath = self.locales_directory_path + bird_name_filename
    if os.path.isfile(bird_name_filepath):
      with open(bird_name_filepath, 'r') as jsonfile:
        return json.load(jsonfile)

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

  def __init__(self, available_locale_codes: list, user_locale_cookie_key):
    self.available_locale_codes = available_locale_codes
    self.user_locale_cookie_key = user_locale_cookie_key

  def determine_locale_from_request(self, request):
    locale_code = self.__determine_from_cookies(request.cookies)
    if not locale_code:
      locale_code = self.__determine_from_headers(request.headers)
    if not locale_code:
      locale_code = next(iter(self.available_locale_codes))
    return locale_code

  def __determine_from_cookies(self, cookies):
    cookie_locale_code = cookies.get(self.user_locale_cookie_key)
    if cookie_locale_code in self.available_locale_codes:
      return cookie_locale_code

  def __determine_from_headers(self, headers):
    if 'Accept-Language' in headers:
      header = headers['Accept-Language']
      requested_codes = list(map(lambda c: c.split(';')[0], header.split(',')))
      available_codes = self.available_locale_codes
      matching_codes = filter(lambda c: c in available_codes, requested_codes)
      return next(matching_codes, None)