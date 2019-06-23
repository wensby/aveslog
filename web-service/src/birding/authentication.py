import os
from base64 import b64encode
from .mail import EmailAddress
from flask import url_for

class AccountRegistrationController:

  def __init__(self, account_repository, mail_dispatcher, link_factory, person_repository):
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory
    self.person_repository = person_repository

  def initiate_registration(self, raw_email, locale):
    if EmailAddress.is_valid(raw_email):
      email = EmailAddress(raw_email)
      registration = self.account_repository.create_account_registration(email.address)
      self.__send_registration_email(email, registration, locale)
      return registration
    return 'invalid email'

  def __send_registration_email(self, email_address, registration, locale):
    token = registration.token
    link = self.link_factory.create_endpoint_external_link('authentication.get_register_form', token=token)
    message = self.create_registration_mail_message(link, locale)
    self.mail_dispatcher.dispatch(email_address.address, 'Birding Registration', message)

  def create_registration_mail_message(self, link, locale):
    message = (
        'Hi there, thanks for showing interest in birding. '
        'Here is your link to the registration form: ')
    return locale.text(message) + link

  def perform_registration_request(self, request):
    registration = self.__find_associated_registration(request)
    if not registration:
      return 'associated registration missing'
    if self.account_repository.find_user_account(request.username):
      return 'username taken'
    account = self.__create_account(request)
    if account:
      self.__remove_registration(registration.id)
      self.__initialize_account_person(account)
      return 'success'
    return 'failure'

  def __find_associated_registration(self, request):
    email = request.email
    token = request.registration_token
    return self.account_repository.find_account_registration(email, token)

  def __create_account(self, request):
    email = request.email
    username = request.username
    password = request.password
    return self.account_repository.put_new_user_account(email, username, password)

  def __remove_registration(self, registration_id):
    self.account_repository.remove_account_registration_by_id(registration_id)

  def __initialize_account_person(self, account):
    person = self.person_repository.add_person(account.username)
    self.account_repository.set_user_account_person(account, person)

class AccountRegistrationRequest:

  def __init__(self, email, registration_token, username, password):
    self.email = email
    self.registration_token = registration_token
    self.username = username
    self.password = password

class PasswordResetController:

  def __init__(self, account_repository, password_repository, link_factory, mail_dispatcher):
    self.account_repository = account_repository
    self.password_repository = password_repository
    self.link_factory = link_factory
    self.mail_dispatcher = mail_dispatcher

  def initiate_password_reset(self, email, locale):
    account = self.account_repository.find_account_by_email(email)
    if account:
      password_reset_token = self.password_repository.create_password_reset_token(account)
      token = password_reset_token.token
      link = self.link_factory.create_endpoint_external_link('authentication.get_password_reset_form', token=token)
      message = self.__create_mail_message(link, locale)
      self.mail_dispatcher.dispatch(email, 'Birding Password Reset', message)
      return True
    return False

  def __create_mail_message(self, link, locale):
    message = (
        'You have requested a password reset of your Birding account. '
        'Please follow this link to get to your password reset form: ')
    return locale.text(message) + link

  def perform_password_reset(self, token, password):
    account_id = self.password_repository.find_password_reset_account_id(token)
    if account_id:
      self.password_repository.update_password(account_id, password)
      self.password_repository.remove_password_reset_token(token)
      return 'success'

class SaltFactory:

  def create_salt(self):
    return b64encode(os.urandom(16)).decode('utf-8')
