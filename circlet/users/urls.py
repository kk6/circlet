# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.TwitterLoginRedirectView.as_view(), name="login"),
    path("callback/", views.TwitterCallbackRedirectView.as_view(), name="callback"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "fetch_twitter_followings/",
        views.FetchTwitterFollowingsRedirectView.as_view(),
        name="fetch_twitter_followings",
    ),
]
