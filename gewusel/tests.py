from django.test import TestCase
from gewusel.models import *

import logging
logger = logging.getLogger(__name__)

class GameTestCase(TestCase):
  def setUp(self):
    Game.objects.create(name="test")

  def test_game_created(self):
    game = Game.objects.get(name="test")
    self.assertEqual(game.name, 'test')

class CountryTestCase(TestCase):
  def setUp(self):
    Country.objects.create(country_code='AT', nicename='Austria')

  def test_country_created(self):
    o = Country.objects.get(country_code='AT')
    self.assertEqual(o.nicename, 'Austria')

class GroupTestCase(TestCase):
  def setUp(self):
    Country.objects.create(country_code='AT', nicename='Austria')
    g = Group.objects.create(
      name='test',
      country=Country.objects.get(country_code='AT')
    )

  def test_group_created(self):
    o = Group.objects.get(name='test')
    self.assertEqual(o.name, 'test')
    self.assertEqual(o.get_absolute_url(), '/gewusel/group/1/')
