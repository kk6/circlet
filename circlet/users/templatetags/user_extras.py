# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='full')
def get_full_size_profile_image(url):
    return url.replace("_normal", "")
