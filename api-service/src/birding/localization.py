from __future__ import annotations
import json
import os
from typing import Optional, List, Union, Any, Set
from flask import Request
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .sqlalchemy_database import Base
from .bird import Bird


def replace_text_variables(text: str, variables: List[str] = None) -> str:
  if variables:
    i = 0
    while '{{}}' in text:
      text = text.replace('{{}}', variables[i], 1)
      i += 1
  return text


class Locale(Base):
  __tablename__ = 'locale'
  id = Column(Integer, primary_key=True)
  code = Column(String, nullable=False)

  def __repr__(self) -> str:
    return f"<Locale(code='{self.code}')>"

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, self.__class__):
      return self.id == other.id and self.code == other.code
    return False

  def __hash__(self) -> int:
    return hash(self.id) ^ hash(self.code)


class LoadedLocale:

  def __init__(self,
        locale: Locale,
        dictionary: Optional[dict],
        bird_dictionary: Optional[dict],
        misses_repository: Optional[dict]) -> None:
    self.locale = locale
    self.dictionary = dictionary
    self.bird_dictionary = bird_dictionary
    self.misses_repository = misses_repository

  def text(self, text: str, variables: List[str] = None) -> str:
    translation = self.__find_translation(text)
    if translation:
      return replace_text_variables(translation, variables)
    else:
      self.__record_text_miss(text)
      return replace_text_variables(text, variables)

  def __find_translation(self, text: str) -> Optional[str]:
    if self.dictionary and text in self.dictionary:
      return self.dictionary[text]

  def __record_text_miss(self, text: str) -> None:
    if not self.misses_repository is None:
      self.misses_repository.setdefault(self.locale, set()).add(text)

  def name(self, bird: Union[Bird, str]) -> str:
    binomial_name = bird.binomial_name if isinstance(bird, Bird) else bird
    if self.bird_dictionary and binomial_name in self.bird_dictionary:
      return self.bird_dictionary[binomial_name]
    else:
      return binomial_name


class LocaleLoader:

  def __init__(self,
        locales_directory_path: str,
        locales_misses_repository: dict) -> None:
    self.locales_directory_path = locales_directory_path
    self.locales_misses_repository = locales_misses_repository

  def load_locale(self, locale: Locale) -> LoadedLocale:
    language_dictionary = self.load_dictionary(locale)
    bird_dictionary = self.load_bird_dictionary(locale)
    return LoadedLocale(
      locale, language_dictionary, bird_dictionary,
      self.locales_misses_repository)

  def load_dictionary(self, locale: Locale) -> Optional[dict]:
    locale_directory_path = self.locale_directory_path(locale)
    return self.load_dict(f'{locale_directory_path}/{locale.code}.json')

  def load_bird_dictionary(self, locale: Locale) -> Optional[dict]:
    locale_directory_path = self.locale_directory_path(locale)
    file_path = f'{locale_directory_path}/{locale.code}-bird-names.json'
    return self.load_dict(file_path)

  def load_dict(self, file_path: str) -> Optional[dict]:
    if os.path.exists(file_path):
      with open(file_path, 'r') as file:
        return json.load(file)

  def locale_directory_path(self, locale: Locale) -> str:
    return f'{self.locales_directory_path}/{locale.code}'


class LocaleRepository:

  def __init__(self,
        locales_directory_path: str,
        locale_loader: LocaleLoader,
        sqlalchemy_session: Session,
  ):
    self.locales_directory_path = locales_directory_path
    self.locale_loader = locale_loader
    self.session = sqlalchemy_session

  def available_locale_codes(self) -> Set[str]:
    is_length_2 = lambda x: len(x) == 2
    return set(filter(is_length_2, self.__locales_directory_subdirectories()))

  def __locales_directory_subdirectories(self) -> List[str]:
    path = self.locales_directory_path
    is_dir = lambda x: os.path.isdir(os.path.join(path, x))
    return list(filter(is_dir, self.__locales_directory_files()))

  def __locales_directory_files(self) -> List[str]:
    path = self.locales_directory_path
    if not os.path.isdir(path):
      return []
    return os.listdir(path)

  def enabled_locale_codes(self) -> List[str]:
    return list(map(lambda l : l.code, self.locales))

  def find_locale_by_code(self, code: str) -> Optional[Locale]:
    return self.session.query(Locale).filter_by(code=code).first()

  @property
  def locales(self) -> List[Locale]:
    return self.session.query(Locale).all()


class LocaleDeterminerFactory:

  def __init__(self,
        user_locale_cookie_key: str,
        locale_repository: LocaleRepository) -> None:
    self.user_locale_cookie_key = user_locale_cookie_key
    self.locale_repository = locale_repository

  def create_locale_determiner(self) -> LocaleDeterminer:
    enabled = self.locale_repository.enabled_locale_codes()
    return LocaleDeterminer(self.user_locale_cookie_key, enabled)


class LocaleDeterminer:

  def __init__(self, user_locale_cookie_key: str, locale_codes: list) -> None:
    self.user_locale_cookie_key = user_locale_cookie_key
    self.locale_codes = locale_codes

  def determine_locale_from_request(self, request: Request) -> Optional[str]:
    if not self.locale_codes:
      return None
    locale_code = self.__determine_from_cookies(request.cookies)
    if not locale_code:
      locale_code = self.__determine_from_headers(request.headers)
    if not locale_code:
      locale_code = next(iter(self.locale_codes), None)
    return locale_code

  def __determine_from_cookies(self, cookies: dict) -> Optional[str]:
    cookie_locale_code = cookies.get(self.user_locale_cookie_key)
    if cookie_locale_code in self.locale_codes:
      return cookie_locale_code

  def __determine_from_headers(self, headers: dict) -> Optional[str]:
    if 'Accept-Language' in headers:
      header = headers['Accept-Language']
      requested_codes = list(map(lambda c: c.split(';')[0], header.split(',')))
      matching_codes = filter(lambda c: c in self.locale_codes, requested_codes)
      return next(matching_codes, None)
