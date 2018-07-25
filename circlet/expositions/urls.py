# -*- coding: utf-8 -*-
from django.urls import path
from .views import ExpositionListView

urlpatterns = [
    path('', ExpositionListView.as_view(), name='exposition_list'),
]