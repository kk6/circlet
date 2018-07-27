# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class TwitterAccount(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField("Name", max_length=100)
    screen_name = models.CharField("Screen name", max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} [@{self.screen_name}]"

    class Meta:
        db_table = "twitter_accounts"


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    twitter_account = models.OneToOneField(TwitterAccount, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"<UserSettings:{self.id}:{self.user.username}>"

    class Meta:
        db_table = "user_settings"
