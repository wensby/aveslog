from unittest import TestCase
from birding.sighting import Sighting
from datetime import date


class TestSighting(TestCase):

  def test_eq_false_when_other_type(self):
    sighting = Sighting(
      id=4, birder_id=8, bird_id=15,
      sighting_date=date(2019, 7, 12), sighting_time=None)
    self.assertNotEqual(sighting, 'Sighting(4, 8, 15, date(2019, 7, 12), None)')

  def test_repr(self):
    sighting = Sighting(
      id=4, birder_id=8, bird_id=15,
      sighting_date=date(2019, 7, 12), sighting_time=None)
    self.assertEqual(
      repr(sighting), (
        "<Sighting(birder_id='8', bird_id='15', "
        "sighting_date='2019-07-12', sighting_time='None')>"))
