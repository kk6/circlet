# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TwitterAccount, UserSettings


@admin.register(TwitterAccount)
class TwitterAccountAdmin(admin.ModelAdmin):
    search_fields = ["name", "screen_name"]


@admin.register(UserSettings)
class UserSettingsAddmin(admin.ModelAdmin):
    pass
