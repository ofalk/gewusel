# Imports
from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.utils.translation import (
  LANGUAGE_SESSION_KEY, TranslatorCommentWarning, trim_whitespace,
)
from django.utils import translation
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, ProcessFormView
from django.forms.models import model_to_dict
from django.db.models import Sum
from django.contrib.auth.models import User

from pfadi import settings

# Internal includes
from gewusel.forms import *
from .models import *

# Additional imports
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def setsuperuser(request):
  if request.user.is_authenticated:
    try:
      if request.user.email in settings.ADMIN_USERS:
        if request.user.is_superuser == False:
          logger.warning("Setting %s (%s) superuser" % (request.user.username, request.user.email, ))
          request.user.is_staff = True
          request.user.is_superuser = True
          request.user.save();
      else:
        if request.user.is_superuser:
          logger.warning("Revoking superuser access rights for %s (%s)" % (request.user.username, request.user.email, ))
          request.user.is_staff = False
          request.user.is_superuser = False
          request.user.save()
    except:
      pass

def logout(request):
    auth_logout(request)
    return redirect('/')

class GewuselView(ListView):
  def get_context_data(self, **kwargs):
    setsuperuser(self.request)
    try:
      logger.warning("Activating '%s' as the language" % self.request.session[settings.LANGUAGE_SESSION_KEY])
      translation.activate(self.request.session[settings.LANGUAGE_SESSION_KEY])
    except:
      pass
    context = super(ListView, self).get_context_data(**kwargs)
    return context

  def get_queryset(self):
    try:
      return self.model.objects.filter(pk=self.kwargs['pk'])
    except:
      return self.model.objects.filter()

  def render_to_response(self, context):
    if self.kwargs:
      try:
        if self.kwargs['format'] == 'json':
          return self.json()
        else:
           return super(GewuselView, self).render_to_response(context)
      except Exception as e:
        logger.warning("Exception: %s" % e)
    return super(GewuselView, self).render_to_response(context)

@method_decorator(login_required, name='dispatch')
class SettingView(GewuselView):
  model = Setting
  template_name = "setting.html"

@method_decorator(login_required, name='dispatch')
class PatrolView(GewuselView):
  model = Patrol
  template_name = "patrol.html"

  def post(self, request, *args, **kwargs):
    # logger.warning(request.is_ajax()); # is ajax request
    json_data = json.loads(request.body.decode('utf-8'))
    objects = Patrol.objects.all()
    if(json_data['group'] != ""):
      objects = Patrol.objects.filter(group__pk = json_data['group'])
    else:
      if(json_data['country'] != ""):
        objects = Patrol.objects.filter(group__country__pk = json_data['country'])

    returnObject = []
    for object in objects:
      returnObject.append({
        'pk': object.pk,
        'name': object.name,
        'group_name': object.group.name,
        'group_id': object.group.pk,
      })
    return JsonResponse({"objects": returnObject}, safe=False)

  def json(self):
    if self.kwargs['pk'] == '0':
      objects = self.model.objects.all().order_by('name')
    else:
      objects = self.model.objects.filter(group__pk=self.kwargs['pk']).order_by('name')
    returnObject = []
    for object in objects:
      returnObject.append({
        'pk': object.pk,
        'name': object.name,
        'group_name': object.group.name,
        'group_id': object.group.pk,
        })
    return JsonResponse({"objects": returnObject}, safe=False)

@method_decorator(login_required, name='dispatch')
class GroupView(GewuselView):
  model = Group
  template_name = "group.html"

  def json(self):
    objects = self.model.objects.filter(country__pk=self.kwargs['pk']).order_by('name')
    returnObject = []
    for object in objects:
      returnObject.append({ 'pk': object.pk, 'name': object.name})
    return JsonResponse({"objects": returnObject}, safe=False)

@method_decorator(login_required, name='dispatch')
class SubcampView(GewuselView):
  model = Subcamp
  template_name = "subcamp.html"

@method_decorator(login_required, name='dispatch')
class SubcampPatrolStats(GewuselView):
  model = Subcamp
  template_name = "subcamp_patrol_stats.html"

  def get_context_data(self, **kwargs):
    context = super(SubcampPatrolStats, self).get_context_data(**kwargs)
    context['patrols'] = self.model.objects.filter(pk=self.kwargs['pk']).values('patrol__name', 'patrol__group__name', 'name').annotate(Sum('patrol__points__points')).order_by('-patrol__points__points__sum', 'patrol__name')
    return context

class PointsView(GewuselView):
  model = Points
  template_name = "points.html"

  def json(self):
    objects = []
    if self.kwargs:
      try:
        if self.kwargs['pk']:
          objects = self.model.objects.filter(pk__gt = self.kwargs['pk'])
      except:
        objects = self.model.objects.order_by('-datetime_entered')[:10]
    else:
      objects = self.model.objects.order_by('-datetime_entered')[:10]

    returnObject = []
    for object in objects:
      returnObject.append({
        'pk':               object.pk,
        'points':           object.points,
        'datetime_entered': object.datetime_entered,
        'patrol':           json.dumps(model_to_dict(object.patrol)),
        'game':             json.dumps(model_to_dict(object.game)),
      })
    return JsonResponse({"objects": returnObject}, safe=False)

class GewuselEdit(PermissionRequiredMixin, UpdateView, ProcessFormView):
  def get_context_data(self, **kwargs):
    try:
      translation.activate(self.request.session[settings.LANGUAGE_SESSION_KEY])
    except:
      pass
    context = super(UpdateView, self).get_context_data(**kwargs)
    return context

class SettingEdit(GewuselEdit):
  model = Setting
  form_class = SettingForm
  template_name = 'setting_edit.html'
  permission_required = 'gewusel.change_setting'

class PatrolEdit(GewuselEdit):
  model = Patrol
  form_class = PatrolForm
  template_name = 'patrol_edit.html'
  permission_required = 'gewusel.change_patrol'

class GroupEdit(GewuselEdit):
  model = Group
  form_class = GroupForm
  template_name = 'group_edit.html'
  permission_required = 'gewusel.change_group'

class SubcampEdit(GewuselEdit):
  model = Subcamp
  form_class = SubcampForm
  template_name = 'subcamp_edit.html'
  permission_required = 'gewusel.change_subcamp'

class GewuselCreate(PermissionRequiredMixin, CreateView):
  def get_context_data(self, **kwargs):
    try:
      translation.activate(self.request.session[settings.LANGUAGE_SESSION_KEY])
    except:
      pass
    context = super(UpdateView, self).get_context_data(**kwargs)
    return context

class Points(PermissionRequiredMixin, CreateView):
  model = Points
  form_class = PointsForm

  def form_valid(self, form):
    form.instance.entered_by = self.request.user
    return super(CreateView, self).form_valid(form)
  def get_context_data(self, **kwargs):
    try:
      translation.activate(self.request.session[settings.LANGUAGE_SESSION_KEY])
    except:
      pass
    context = super(Points, self).get_context_data(**kwargs)
    return context

class PointsEdit(Points, UpdateView):
  permission_required = 'gewusel.change_points'
  template_name = 'points_edit.html'

class PointsAdd(Points, CreateView):
  permission_required = 'gewusel.add_points'
  template_name = 'points_add.html'

class StatsView(TemplateView):
  template_name = 'stats.html'

  def get_context_data(self, **kwargs):
    try:
      translation.activate(self.request.session[settings.LANGUAGE_SESSION_KEY])
    except:
      pass
    context = super(TemplateView, self).get_context_data(**kwargs)
    return context

class TopView(ListView):
  template_name = 'top.html'
  from gewusel.models import Points
  model = Points
  queryset = Points.objects.all()

  def get_context_data(self, **kwargs):
    try:
      translation.activate(self.request.session[settings.LANGUAGE_SESSION_KEY])
    except:
      pass
    context = super(ListView, self).get_context_data(**kwargs)
    context['setting'] = Setting.objects
    return context

class TopPatrolsView(ListView):
  from gewusel.models import Points
  model = Points
  queryset = Points.objects.all()

  def render_to_response(self, context):
    objects = self.model.objects.values('patrol').annotate(sum=Sum('points')).order_by('-sum')[:10]

    returnObject = []
    for object in objects:
      patrol = Patrol.objects.get(pk=object['patrol'])
      object['patrol_name'] = patrol.name
      object['patrol_id'] = patrol.pk
      object['group_name'] = patrol.group.name
      object['group_id'] = patrol.group.pk
      returnObject.append(object)
    return JsonResponse({"objects": returnObject}, safe=False)

class TopSubcampsView(ListView):
  from gewusel.models import Subcamp
  model = Subcamp
  queryset = Subcamp.objects.all()

  def render_to_response(self, context):
    from gewusel.models import Patrol as PatrolModel
    objects = self.model.objects.by_points()[:10]

    returnObject = []
    for object in objects:
      obj = {}
      obj['subcamp_id'] = object.pk
      obj['subcamp_name'] = object.name
      obj['points_sum'] = object.points_sum
      obj['patrol_count'] = PatrolModel.objects.filter(subcamp=object.pk).count()

      if object.points_sum != None:
        returnObject.append(obj)
    return JsonResponse({"objects": returnObject}, safe=False)
