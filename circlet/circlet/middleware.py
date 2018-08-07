# -*- coding: utf-8 -*-
from django.shortcuts import redirect

from services.twitter import get_api


class TwitterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ in ("login", "callback"):
            return None
        elif view_func.__name__ == "TemplateView" and request.path_info == "/":
            return None

        if not hasattr(request, "user"):
            return redirect("index")

        tokens = request.session.get("access_token_data")
        if tokens:
            request.twitter_api = get_api(
                tokens["access_token"], tokens["access_token_secret"]
            )
        else:
            return redirect("index")
