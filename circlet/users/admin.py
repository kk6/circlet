# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import TwitterAccount, UserSettings, Friendship


@admin.register(TwitterAccount)
class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "screen_name"]
    search_fields = ["name", "screen_name"]


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "twitter_account"]


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "twitter_account"]
