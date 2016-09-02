from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Sum

# Create your models here.

class SettingManager(models.Manager):
  def get_by_natural_key(self, key):
    return self.get(setting=key)
  def stats_viewable(self):
    return self.get_by_natural_key('stats_viewable').value

class Setting(models.Model):
  objects = SettingManager()

  setting = models.CharField(max_length=80, unique=True)
  value = models.CharField(max_length=80)

  def natural_key(self):
    return (self.setting,)

  def get_absolute_url(self):
    return reverse('setting-view-single', kwargs={'pk': self.pk})

  def __str__(self):
    return self.setting

class CountryManager(models.Manager):
  def get_by_natural_key(self, country):
    return self.get(country_code=country)

class Country(models.Model):
  objects = CountryManager()

  country_code = models.CharField(max_length=2, unique=True)
  nicename = models.CharField(max_length=80)

  def natural_key(self):
    return (self.country_code,)

  def __str__(self):
    return self.nicename

class GroupManager(models.Manager):
  def get_by_natural_key(self, name, country):
    return self.get(name=name, country__country_code=country)

class Group(models.Model):
  objects = GroupManager()

  name = models.CharField(max_length=200)
  country = models.ForeignKey(Country, on_delete=models.CASCADE)

  def natural_key(self):
    return (self.name,) + self.country.natural_key()
  natural_key.dependencies = ['gewusel.country']

  class Meta:
    unique_together = (('name', 'country'),)
    ordering = ['country__nicename','name']

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('group-view-single', kwargs={'pk': self.pk})

class SubcampManager(models.Manager):
  def get_by_natural_key(self, name):
    return self.get(name=name)

  def by_points(self, *args, **kwargs):
    qs = super(SubcampManager, self).get_queryset(*args, **kwargs)
    ordered = qs.annotate(points_sum=Sum('patrol__points__points')).order_by('-points_sum')
    return ordered

class Subcamp(models.Model):
  objects = SubcampManager()

  name = models.CharField(max_length=100, unique=True)
  class Meta:
    ordering = ['name']

  def natural_key(self):
    return (self.name,)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('subcamp-view-single', kwargs={'pk': self.pk})

class PatrolManager(models.Manager):
  def get_by_natural_key(self, name, group):
    return self.get(name=name, group__name=group)

class Patrol(models.Model):
  objects = PatrolManager()

  name = models.CharField(max_length=200)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  subcamp = models.ForeignKey(Subcamp, on_delete=models.CASCADE)

  def natural_key(self):
    return (self.name,self.group)
  natural_key.dependencies = ['gewusel.group']
  class Meta:
    unique_together = (('name', 'group'),)
    ordering = ['subcamp__name','group__country__nicename','group__name']

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('patrol-view-single', kwargs={'pk': self.pk})

class Game(models.Model):
  name = models.CharField(max_length=200)
  class Meta:
    ordering = ['name']

  def __str__(self):
    return self.name

class Points(models.Model):
  points = models.PositiveSmallIntegerField()
  patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  datetime_entered = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
  entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)

  class Meta:
    ordering = ['-datetime_entered']

  def __str__(self):
    return str(self.points)
  def get_absolute_url(self):
    return reverse('points-view-single', kwargs={'pk': self.pk})
