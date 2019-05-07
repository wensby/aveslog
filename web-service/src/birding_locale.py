language_dictionaries = {
    'en': {'Search bird': 'Search bird'},
    'se': {'Search bird': 'Sök fågel'},
    'ko': {'Search bird': '새 검색'}
}

def figure_out_language_from_request_cookies(cookies):
  user_lang = cookies.get('user_lang')
  if user_lang in language_dictionaries.keys():
    return user_lang

def figure_out_language_from_request_headers(headers):
  supported = supported_languages()
  if 'Accept-Language' in headers:
    requested = headers['Accept-Language'].split(',')
    matches = filter(lambda x: x.split(';')[0] in supported, requested)
    return next(matches, supported[0]).split(';')[0]
  return supported[0]

def figure_out_language_from_request(request):
  language = figure_out_language_from_request_cookies(request.cookies)
  if language is None:
    language = figure_out_language_from_request_headers(request.headers)
  return language

def supported_languages():
  return [k for k in language_dictionaries]
