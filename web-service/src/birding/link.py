from flask import url_for

class LinkFactory:

  def __init__(self, external_host):
    self.external_host = external_host

  def create_url_external_link(self, url):
    return f'{self.external_host}{url}'

  def create_endpoint_external_link(self, endpoint, **values):
    return self.create_url_external_link(url_for(endpoint, **values))
