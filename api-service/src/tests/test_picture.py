from unittest import TestCase

from birding.picture import Picture


class TestPicture(TestCase):

  def test_construction(self):
    Picture(4, 'myFilepath', 'myCredit')

  def test_fromrow(self):
    picture = Picture.fromrow([4, 'myFilepath', 'myCredit'])
    self.assertEqual(picture, Picture(4, 'myFilepath', 'myCredit'))

  def test_eq_false_when_other_type(self):
    self.assertNotEqual(Picture(4, 'a', 'b'), 'Picture(4, a, b)')

  def test_repr(self) -> None:
    self.assertEqual(repr(Picture(1, 'a', 'b')), 'Picture(1, a, b)')