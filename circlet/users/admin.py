# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TwitterAccount


@admin.register(TwitterAccount)
class TwitterAccountAdmin(admin.ModelAdmin):
    search_fields = ["name", "screen_name"]
