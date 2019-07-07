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
    bird_dictionary_filepath = (
        f'{self.locales_directory_path}/{lang_iso}/{lang_iso}-bird-names.json')
    if os.path.exists(bird_dictionary_filepath):
      with open(bird_dictionary_filepath, 'r') as file:
        bird_dictionary = json.load(file)
    return Locale(lang_iso, language_dictionary, bird_dictionary)

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
      return list(map(lambda x: x[1], result.rows))

  def find_locale_by_id(self, id):
    with self.database.transaction() as transaction:
      result = transaction.execute('SELECT code FROM locale WHERE id = %s;', (id, ))
      return self.find_locale(result.rows[0][0])

  def find_locale(self, code):
    return self.locale_loader.load_locale(code)


class Locale:

  def __init__(self, code, dictionary, bird_dictionary):
    self.code = code
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


class LocaleDeterminerFactory:

  def __init__(self,
        user_locale_cookie_key: str,
        locale_repository : LocaleRepository):
    self.user_locale_cookie_key = user_locale_cookie_key
    self.locale_repository = locale_repository

  def create_locale_determiner(self):
    available = self.locale_repository.available_locale_codes()
    enabled = self.locale_repository.enabled_locale_codes()
    locale_codes = list(filter(lambda locale: locale in enabled, available))
    return LocaleDeterminer(self.user_locale_cookie_key, locale_codes)

class LocaleDeterminer:

  def __init__(self,
        user_locale_cookie_key,
        locale_codes: list):
    self.user_locale_cookie_key = user_locale_cookie_key
    self.locale_codes = locale_codes

  def determine_locale_from_request(self, request):
    if not self.locale_codes:
      return None
    locale_code = self.__determine_from_cookies(request.cookies)
    if not locale_code:
      locale_code = self.__determine_from_headers(request.headers)
    if not locale_code:
      locale_code = next(iter(self.locale_codes), None)
    return locale_code

  def __determine_from_cookies(self, cookies):
    cookie_locale_code = cookies.get(self.user_locale_cookie_key)
    if cookie_locale_code in self.locale_codes:
      return cookie_locale_code

  def __determine_from_headers(self, headers):
    if 'Accept-Language' in headers:
      header = headers['Accept-Language']
      requested_codes = list(map(lambda c: c.split(';')[0], header.split(',')))
      matching_codes = filter(lambda c: c in self.locale_codes, requested_codes)
      return next(matching_codes, None)