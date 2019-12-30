from aveslog.nominatim import Nominatim


def create_geocoding(testing):
  if testing:
    return MockedGeocoding()
  else:
    nominatim = Nominatim()
    return NominatimGeocoding(nominatim)


class ReverseSearchResult:

  def __init__(
        self,
        coordinates: tuple,
        language_code: str,
        detail_level: int,
        name: str,
  ):
    self.coordinates = coordinates
    self.language_code = language_code
    self.detail_level = detail_level
    self.name = name


class Geocoding:

  def reverse_search(self, coordinates: tuple) -> ReverseSearchResult:
    pass


class NominatimGeocoding(Geocoding):

  def __init__(self, nominatim: Nominatim):
    self._nominatim = nominatim

  def reverse_search(self, coordinates) -> ReverseSearchResult:
    lat, lon = coordinates
    language_code = 'en-EN'
    detail_level = 18
    nominatim_response = self._nominatim.reverse(
      lat,
      lon,
      zoom=detail_level,
      language=language_code,
    )
    if nominatim_response:
      result_coordinates = (
        nominatim_response['lat'],
        nominatim_response['lon'],
      )
      display_name = nominatim_response['display_name']
      return ReverseSearchResult(
        result_coordinates,
        language_code,
        detail_level,
        display_name,
      )


class MockedGeocoding(Geocoding):

  def reverse_search(self, coordinates) -> ReverseSearchResult:
    return ReverseSearchResult(coordinates, 'en-EN', 18, f'{coordinates} name')
