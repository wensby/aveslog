from unittest import TestCase

from birding.picture import Picture


class TestPicture(TestCase):

  def test_construction(self):
    Picture(4, 'myFilepath', 'myCredit')