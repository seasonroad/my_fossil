# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from fossil_app.views import *


urlpatterns = patterns('fossil_app.views',
    url(r'^$', FossilPlantView.as_view(), name='fossil_home'),
    url(r'^fossilplant/$', FossilPlantView.as_view(), name='fossil'),
    url(r'^fossilanimal/$', FossilPlantView.as_view(), name='fossil'),
    url(r'^fossilplant/tree/(?P<node_id>\w+)/$', FossilSelectView.as_view(), name='fossil'),

    url(r'^fossilplant/add_node/(?P<node_id>\w+)/$', FossilAddNodeView.as_view(), name='fossil'),
    url(r'^fossilplant/add_node/$', FossilAddNodeView.as_view(), name='add_node'),
)
