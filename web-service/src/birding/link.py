class LinkFactory:

  def __init__(self, external_host):
    self.external_host = external_host

  def create_external_link(self, url):
    return f'{self.external_host}{url}'
