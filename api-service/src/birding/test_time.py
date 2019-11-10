from datetime import time
from unittest import TestCase

from birding.time import parse_time


class TestTime(TestCase):

  def test_parse_time_parses_iso_format_correctly(self):
    self.assertEqual(parse_time('19:03'), time(19, 3))
