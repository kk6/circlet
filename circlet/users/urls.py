# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "fetch_twitter_followings/",
        views.FetchTwitterFollowingsRedirectView.as_view(),
        name="fetch_twitter_followings",
    ),
]
