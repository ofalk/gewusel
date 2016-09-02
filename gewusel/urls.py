from django.conf.urls import url

from . import views
from gewusel.views import *
urlpatterns = [
    url(r'^$', TopView.as_view(), name='index'),

    #### Class based views
    url(r'^setting/(?P<pk>\w+)/$',                     SettingView.as_view(), name='setting-view-single'),
    url(r'^setting/$',                                 SettingView.as_view(), name='setting-view-all'),
    url(r'^setting/(?P<pk>\w+)/edit/$',                SettingEdit.as_view(), name='setting-edit'),

    url(r'^patrol/(?P<pk>\w+)/$',                      PatrolView.as_view(),  name='patrol-view-single'),
    url(r'^patrol/$',                                  PatrolView.as_view(),  name='patrol-view-all'),
    url(r'^patrol/(?P<pk>\w+)/edit/$',                 PatrolEdit.as_view(),  name='patrol-edit'),
    url(r'^patrol/(?P<pk>\w+)/(?P<format>json)/$',     PatrolView.as_view(),  name='patrol-json'),

    url(r'^group/(?P<pk>\w+)/$',                       GroupView.as_view(),   name='group-view-single'),
    url(r'^group/$',                                   GroupView.as_view(),   name='group-view-all'),
    url(r'^group/(?P<pk>\w+)/edit/$',                  GroupEdit.as_view(),   name='group-edit'),
    url(r'^group/(?P<pk>\w+)/(?P<format>json)/$',      GroupView.as_view(),   name='group-json'),

    url(r'^subcamp/(?P<pk>\w+)/$',                     SubcampView.as_view(),        name='subcamp-view-single'),
    url(r'^subcamp/$',                                 SubcampView.as_view(),        name='subcamp-view-all'),
    url(r'^subcamp/(?P<pk>\w+)/edit/$',                SubcampEdit.as_view(),        name='subcamp-edit'),
    url(r'^subcamp/(?P<pk>\w+)/stats/$',               SubcampPatrolStats.as_view(), name='subcamp-patrol-stats'),

    url(r'^points/add/$',                              PointsAdd.as_view(),   name='points-add'),
    url(r'^points/(?P<pk>\w+)/edit/$',                 PointsEdit.as_view(),  name='points-edit'),
    url(r'^points/(?P<format>json)/$',                 PointsView.as_view(),  name='points-json'),
    url(r'^points/(?P<format>json)/(?P<pk>[0-9]+)/$',  PointsView.as_view(),  name='points-json'),
    url(r'^points/(?P<pk>\w+)/$',                      PointsView.as_view(),  name='points-view-single'),
    url(r'^points/$',                                  PointsView.as_view(),  name='points-view-all'),

    url(r'^stats/$',                                   StatsView.as_view(),       name='stats'),
    url(r'^stats/toppatrols/$',                        TopPatrolsView.as_view(),  name='toppatrols'),
    url(r'^stats/topsubcamps/$',                       TopSubcampsView.as_view(), name='topsubcamps'),
    url(r'^stats/top/$',                               TopView.as_view(),         name='top'),
]
