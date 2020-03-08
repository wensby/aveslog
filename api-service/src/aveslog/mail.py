import os

from flask import Flask
from flask_mail import Mail, Message
from distutils.util import strtobool
import re


def is_valid_email_address(email):
  pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
  return pattern.match(email)


class MailDispatcher():

  def dispatch(self, recipient, subject, body):
    pass


class MailDispatcherFactory:

  def create_dispatcher(self, app: Flask) -> MailDispatcher:
    if 'MAIL_SERVER' in os.environ:
      server = os.environ['MAIL_SERVER']
      port = os.environ['MAIL_PORT']
      username = os.environ['MAIL_USERNAME']
      password = os.environ['MAIL_PASSWORD']
      use_tls = bool(strtobool(os.environ['MAIL_USE_TLS']))
      use_ssl = bool(strtobool(os.environ['MAIL_USE_SSL']))
      return MailServerDispatcher(app, server, port, username, password,
        use_tls, use_ssl)
    else:
      return MailDebugDispatcher(app)


class MailDebugDispatcher(MailDispatcher):

  def __init__(self, app):
    self.app = app

  def dispatch(self, recipient, subject, body):
    self.app.logger.info('dispatching mail to %s: %s - %s', recipient, subject,
      body)


class MailServerDispatcher(MailDispatcher):

  def __init__(self, app, server, port, username, password, use_tls, use_ssl):
    self.sender = username
    app.config['MAIL_SERVER'] = server
    app.config['MAIL_PORT'] = port
    app.config['MAIL_USERNAME'] = self.sender
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = use_tls
    app.config['MAIL_USE_SSL'] = use_ssl
    self.mail = Mail(app)

  def dispatch(self, recipient, subject, body):
    message = Message(subject, recipients=[recipient], body=body,
      sender=self.sender)
    self.mail.send(message)
