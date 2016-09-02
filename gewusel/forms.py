from django import forms
from .models import *
from django.utils.translation import ugettext_lazy as _

import logging
logger = logging.getLogger(__name__)

class SettingForm(forms.ModelForm):
  class Meta:
    model = Setting
    fields = ('setting', 'value')

  setting = forms.CharField(
    label = _('Setting'),
    required = True,
    widget = forms.TextInput(attrs={'class': 'form-control'}),
  )
  value = forms.CharField(
    label = _('Value'),
    required = True,
    widget = forms.TextInput(attrs={'class': 'form-control'}),
  )

class PatrolForm(forms.ModelForm):
  class Meta:
    model = Patrol
    fields = ('name', 'group', 'subcamp')

  name = forms.CharField(
    label = _('Name'),
    required = True,
    widget = forms.TextInput(attrs={'class': 'form-control'}),
  )
  group = forms.ModelChoiceField(
    label = _('Group'),
    required = True,
    widget = forms.Select(attrs={'class': 'form-control'}),
    queryset = Group.objects.all(),
  )
  subcamp = forms.ModelChoiceField(
    label = _('Subcamp'),
    required = True,
    widget = forms.Select(attrs={'class': 'form-control'}),
    queryset = Subcamp.objects.all(),
  )

class GroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ('name', 'country')

  name = forms.CharField(
    label = _('Name'),
    required = True,
    widget = forms.TextInput(attrs={'class': 'form-control'}),
  )
  country = forms.ModelChoiceField(
    label = _('Country'),
    required = True,
    widget = forms.Select(attrs={'class': 'form-control'}),
    queryset = Country.objects.all(),
  )

class SubcampForm(forms.ModelForm):
  class Meta:
    model = Subcamp
    fields = ('name',)

  name = forms.CharField(
    label = _('Name'),
    required = True,
    widget = forms.TextInput(attrs={'class': 'form-control'}),
  )

class PointsForm(forms.ModelForm):
  class Meta:
    model = Points
    fields = ('points','patrol','game','country')

  points = forms.IntegerField(
    label = _('Points'),
    required = True,
    widget = forms.NumberInput(attrs={'class': 'form-control'}),
    min_value = 0,
  )
  patrol = forms.ModelChoiceField(
    label = _('Patrol'),
    required = True,
    widget = forms.Select(attrs={'class': 'form-control'}),
    queryset = Patrol.objects.all(),
  )
  game = forms.ModelChoiceField(
    label = _('Game'),
    required = True,
    widget = forms.Select(attrs={'class': 'form-control'}),
    queryset = Game.objects.all(),
  )
  country = forms.ModelChoiceField(
    label = _('Country'),
    required = False,
    widget = forms.Select(attrs={'class': 'form-control'}),
    queryset = Country.objects.all(),
  )
