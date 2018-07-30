# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip

from django.conf.urls import url
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view


from . import views

router = DefaultRouter()
schema_view = get_swagger_view(title='Rural Norte API')

router.register(r'lotes', views.LoteViewSet, base_name='lote')

urlpatterns = [
    # re_path(r'^docs/$', schema_view),  # documentacao swagger
    re_path('^$', schema_view),  # documentacao swagger
   ]
urlpatterns += router.urls
# urlpatterns = format_suffix_patterns(urlpatterns)
app_name = 'api_v1'
