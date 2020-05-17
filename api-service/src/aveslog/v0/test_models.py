from datetime import date, time
from unittest import TestCase

from aveslog.test_util import AppTestCase
from aveslog.v0 import SessionFactory
from aveslog.v0.models import Birder
from aveslog.v0.models import BirdLook
from aveslog.v0.models import Bird
from aveslog.v0.models import BirdCommonName
from aveslog.v0.models import PasswordResetToken
from aveslog.v0.models import Picture
from aveslog.v0.models import Sighting


class TestBirdCommonName(TestCase):

  def test_repr(self):
    common_name = BirdCommonName(name='Skata')
    self.assertEqual(repr(common_name), "<BirdCommonName(name='Skata')>")


class TestBirder(TestCase):

  def test_repr(self):
    donald_duck = Birder(name='Donald Duck')
    self.assertEqual(repr(donald_duck), "<Birder(name='Donald Duck')>")


class TestPasswordResetToken(TestCase):

  def test_eq(self):
    token = PasswordResetToken(account_id=1, token='token')
    identical = PasswordResetToken(account_id=1, token='token')
    self.assertEqual(token, identical)


class TestPicture(TestCase):

  def test_repr(self):
    mona_lisa = Picture(
      filepath='/louvre-museum/mona-lisa.jpg',
      credit='Leonardo Da Vinci',
    )
    self.assertEqual(
      repr(mona_lisa),
      "<Picture(filepath='/louvre-museum/mona-lisa.jpg', "
      "credit='Leonardo Da Vinci')>"
    )


class TestSighting(TestCase):

  def test_eq(self):
    sighting = Sighting(
      id=1,
      birder_id=2,
      bird_id=3,
      sighting_date=date(2019, 11, 10),
      sighting_time=time(20, 52),
    )
    identical = Sighting(
      id=1,
      birder_id=2,
      bird_id=3,
      sighting_date=date(2019, 11, 10),
      sighting_time=time(20, 52),
    )
    self.assertEqual(sighting, identical)


class TestBirdLook(AppTestCase):

  def test_append_through_bird(self):
    session = SessionFactory(self.database_engine).create_session()
    bird = Bird(binomial_name="Pica pica")

    bird.looks.append(BirdLook())
    session.add(bird)
    session.commit()

    cursor = self.database_connection.cursor()
    cursor.execute("SELECT * FROM bird_look")
    result = cursor.fetchall()
    self.assertListEqual(result, [(1, 1, None, None)])
