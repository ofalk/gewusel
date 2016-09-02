from django.shortcuts import render

from pfadi import settings

from django.utils.translation import LANGUAGE_SESSION_KEY

# DEV only
# import the logging library
import logging

from django.shortcuts import redirect

# Get an instance of a logger
logger = logging.getLogger(__name__)
# EOD

# Create your views here.

from django.http import HttpResponse

def setlang(request, lang = 'en-us'):
  request.session[settings.LANGUAGE_SESSION_KEY] = lang
  logger.warning("Setting lang to %s" % lang)
  next = request.GET.get('next')
  if not next:
    next = '/'
  return redirect(next)
