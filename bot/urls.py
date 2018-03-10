# -*- encoding: utf-8 -*-
from django.conf.urls import url
from . import views as lineBotView

urlpatterns = [
    url(r'^callback', lineBotView.as_view()),
]