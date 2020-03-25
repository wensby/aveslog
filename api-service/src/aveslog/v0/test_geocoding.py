from unittest import TestCase

from aveslog.v0.geocoding import create_geocoding, NominatimGeocoding


class TestGeocoding(TestCase):

  def test_create_geocoding(self):
    geocoding = create_geocoding(False)
    self.assertIsInstance(geocoding, NominatimGeocoding)
