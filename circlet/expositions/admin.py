# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Exposition


@admin.register(Exposition)
class ExpositionAdmin(admin.ModelAdmin):
    pass
