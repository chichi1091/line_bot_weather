# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views as lineBot_view

urlpatterns = [
    url(r'^callback', lineBot_view.LineBotView.as_view()),
]
