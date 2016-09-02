"""pfadi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
import gewusel.views
import pfadi.views

urlpatterns = [
    url(r'^tos/', TemplateView.as_view(template_name="tos.html"), name='tos'),
    url(r'^privacy/', TemplateView.as_view(template_name="privacy.html"), name='privacy'),
    url(r'^profile/$', TemplateView.as_view(template_name="profile.html"), name='profile-view'),
    url(r'^setlang/(?P<lang>[a-z-]+)/', pfadi.views.setlang, name='setlang'),
    url(r'^gewusel/', include('gewusel.urls')),
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^logout/$', gewusel.views.logout),
    url(r'^.*$', RedirectView.as_view(url='/gewusel/', permanent=False), name='index'),
]
