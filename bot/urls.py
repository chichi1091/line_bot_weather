# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^callback', views.callback),
]