from datetime import time, date
from unittest import TestCase

from birding.time import parse_time, format_date_time


class TestTime(TestCase):

  def test_parse_time_parses_iso_format_correctly(self):
    self.assertEqual(parse_time('19:03'), time(19, 3))

  def test_format_date_time_without_time(self):
    self.assertEqual(format_date_time(date(2019, 7, 13)), '2019-07-13')
