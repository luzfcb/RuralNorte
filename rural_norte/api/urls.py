# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip

from django.conf.urls import url, include
from django.urls import path

urlpatterns = [
    path('api/v1/', include('rural_norte.api.api_v1.urls', namespace='api_v1')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
