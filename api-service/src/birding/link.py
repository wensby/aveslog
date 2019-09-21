class LinkFactory:

  def __init__(self, external_host, frontend_host):
    self.external_host = external_host
    self.frontend_host = frontend_host

  def create_url_external_link(self, url):
    return f'{self.external_host}{url}'

  def create_frontend_link(self, link):
    return f'{self.frontend_host}{link}'
