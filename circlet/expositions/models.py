# -*- coding: utf-8 -*-
from django.db import models


class Exposition(models.Model):
    name = models.CharField(max_length=255)
    ruby = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.id}:{self.name}"

    class Meta:
        ordering = ["-id"]
        db_table = "expositions"
