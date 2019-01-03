# -*- coding: utf-8 -*-

from django.conf.urls import url

from predict.views import Predict
from . import views


urlpatterns = [

    url(r'^', Predict.as_view()),
]
