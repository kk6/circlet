# -*- coding: utf-8 -*-
from django.views.generic import ListView
from .models import Exposition


class ExpositionListView(ListView):
    model = Exposition
    template_name = "expositions/list.html"
