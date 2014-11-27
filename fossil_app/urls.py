# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from fossil_app.views import *


urlpatterns = patterns('fossil_app.views',
    url(r'^$', FossilHomeView.as_view(), name='fossil_home'),
)
