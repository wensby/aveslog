from unittest import TestCase

from birding.person import Person


class TestPerson(TestCase):

  def test_construction(self):
    Person(4, 'Donald Duck')
