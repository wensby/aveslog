from unittest import TestCase

from birding.v0.models import Picture


class TestPicture(TestCase):

  def test_construction(self):
    Picture(filepath='myFilepath', credit='myCredit')
