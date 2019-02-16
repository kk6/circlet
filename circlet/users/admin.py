# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import TwitterAccount, UserSettings, Friendship


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(TwitterAccount)
class TwitterAccountAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ["id", "name", "screen_name"]
    search_fields = ["name", "screen_name"]
    actions = ["export_as_csv"]


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "twitter_account"]


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "twitter_account"]
