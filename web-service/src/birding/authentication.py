from .mail import EmailAddress
from flask import url_for

class AccountRegistrationController:

  def __init__(self, account_repository, mail_dispatcher, link_factory):
    self.account_repository = account_repository
    self.mail_dispatcher = mail_dispatcher
    self.link_factory = link_factory

  def prepare_account_registration(self, email):
    if EmailAddress.is_valid(email):
      email = EmailAddress(email)
      self.account_repository.put_user_account_registration(email.address)
      registration = self.account_repository.get_user_account_registration_by_email(email.address)
      token = registration.token
      link = self.link_factory.create_external_link(url_for('authentication.get_register_form', token=token))
      self.mail_dispatcher.dispatch(email.address, 'Birding Registration', 'Link: ' + link)
