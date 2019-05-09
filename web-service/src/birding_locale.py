import json

class Locale:

  def __init__(self, id, dictionary):
    self.id = id
    self.dictionary = dictionary

  def text(self, text, variables=None):
    translated = self.dictionary[text] if text in self.dictionary else text
    if variables:
      i = 0
      while '{{}}' in translated:
        translated = translated.replace('{{}}', variables[i], 1)
        i = i + 1
    return translated

class LocaleRepository:

  def __init__(self, locale_dictionary_path):
    self.locales = dict()
    for lang in ['en', 'se', 'ko']:
      with open(locale_dictionary_path + lang + '.json', 'r') as f:
        self.locales[lang] = Locale(lang, json.load(f))

  def get_locale(self, language):
    return self.locales[language]

  def languages(self):
    return self.locales.keys()

class LocaleDeterminer:

  def __init__(self, locale_repository):
    self.repository = locale_repository

  def figure_out_language_from_request_cookies(self, cookies):
    user_lang = cookies.get('user_lang')
    if user_lang in self.repository.languages():
      return user_lang

  def figure_out_language_from_request_headers(self, headers):
    supported = self.repository.languages()
    if 'Accept-Language' in headers:
      requested = headers['Accept-Language'].split(',')
      matches = filter(lambda x: x.split(';')[0] in supported, requested)
      return next(matches, supported[0]).split(';')[0]
    return supported[0]

  def figure_out_language_from_request(self, request):
    language = self.figure_out_language_from_request_cookies(request.cookies)
    if language is None:
      language = self.figure_out_language_from_request_headers(request.headers)
    return language
