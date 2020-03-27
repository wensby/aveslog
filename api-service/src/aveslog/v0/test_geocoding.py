from unittest import TestCase
from unittest.mock import Mock

from aveslog.nominatim import Nominatim
from aveslog.v0.geocoding import create_geocoding
from aveslog.v0.geocoding import NominatimGeocoding
from aveslog.v0.geocoding import Geocoding


class TestGeocoding(TestCase):

  def test_create_geocoding(self):
    geocoding = create_geocoding(False)
    self.assertIsInstance(geocoding, NominatimGeocoding)

  def test_geocoding_class_methods(self):
    geocoding = Geocoding()
    self.assertIsNone(geocoding.reverse_search((30, 30)))


class TestNominatimGeocoding(TestCase):

  def test_reverse_search_when_ok(self):
    nominatim = Mock(spec=Nominatim)
    nominatim_geocoding = NominatimGeocoding(nominatim)
    nominatim.reverse.return_value = {
      'lat': 1,
      'lon': 2,
      'display_name': 'Ottenby'
    }

    result = nominatim_geocoding.reverse_search((1, 2))

    self.assertEqual(result.name, 'Ottenby')
    self.assertEqual(result.detail_level, 18)
    self.assertEqual(result.language_code, 'en-EN')
    self.assertEqual(result.coordinates, (1, 2))
