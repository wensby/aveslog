from .mail import EmailAddress
from flask import url_for

class AccountRegistrationController:

  def __init__(self, account_repository, mail_dispatcher, link_factory, person_repository):
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory
    self.person_repository = person_repository

  def initiate_registration(self, email):
    if EmailAddress.is_valid(email):
      email = EmailAddress(email)
      self.account_repository.put_user_account_registration(email.address)
      registration = self.account_repository.get_user_account_registration_by_email(email.address)
      token = registration.token
      link = self.link_factory.create_endpoint_external_link('authentication.get_register_form', token=token)
      self.mail_dispatcher.dispatch(email.address, 'Birding Registration', 'Link: ' + link)
      return registration

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
