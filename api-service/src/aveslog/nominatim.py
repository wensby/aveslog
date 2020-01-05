import requests

class Nominatim:

  def __init__(self):
    self._url = 'https://nominatim.openstreetmap.org'

  def reverse(self, lat, lon, zoom=18, language='en-EN'):
    r = requests.get(f'{self._url}/reverse?format=jsonv2&lat={lat}&lon={lon}&zoom={zoom}&accept-language={language}', headers={
      'User-Agent': 'Aveslog.com'
    })
    if r.status_code == 200:
      return r.json()
    else:
      return None