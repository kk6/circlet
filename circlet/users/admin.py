# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TwitterAccount, UserSettings, Friendship


@admin.register(TwitterAccount)
class TwitterAccountAdmin(admin.ModelAdmin):
    search_fields = ["name", "screen_name"]


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    pass
