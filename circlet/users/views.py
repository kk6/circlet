# -*- coding: utf-8 -*-
import tweepy

from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView

from circlet.middleware import get_api

from .models import TwitterAccount, UserSettings


def login(request):
    auth = tweepy.OAuthHandler(
        settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.CALLBACK_URL
    )
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise tweepy.TweepError("Error! Failed to get request token")
    request.session["request_token"] = auth.request_token
    return redirect(redirect_url)


def callback(request):
    verifier = request.GET.get("oauth_verifier")
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.request_token = request.session["request_token"]
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print("Error! Failed to get access token.")
    request.session["access_token_data"] = {
        "access_token": auth.access_token,
        "access_token_secret": auth.access_token_secret,
    }
    api = get_api(auth.access_token, auth.access_token_secret)
    twitter_account = api.me()
    try:
        obj = TwitterAccount.objects.get(id=twitter_account.id)
    except TwitterAccount.DoesNotExist:
        obj = TwitterAccount.objects.create(
            id=twitter_account.id,
            name=twitter_account.name,
            screen_name=twitter_account.screen_name,
        )
    else:
        obj.name = twitter_account.name
        obj.screen_name = twitter_account.screen_name
        obj.save()
    try:
        # FIXME: screen_name は変わることがあるのでこれだとマズい。今はとりあえず。
        user = User.objects.get(username=twitter_account.screen_name)
    except User.DoesNotExist:
        user = User.objects.create_user(username=twitter_account.screen_name)
    user_settings, _ = UserSettings.objects.get_or_create(user=user)
    user_settings.twitter_account = obj
    user_settings.save()
    return redirect("dashboard")


def dashboard(request):
    user = request.twitter_api.me()
    return render(request, "dashboard.html", context={"user": user})


class FetchTwitterFollowingsRedirectView(RedirectView):
    pattern_name = "dashboard"

    def get_redirect_url(self, *args, **kwargs):
        def chunked(ls, size):
            return [ls[x : x + size] for x in range(0, len(ls), size)]

        api = self.request.twitter_api
        user = api.me()
        friends_ids = api.friends_ids(user.id)
        chunked_friends_ids = chunked(friends_ids, 100)
        for friends_ids in chunked_friends_ids:
            friends = api.lookup_users(user_ids=friends_ids)
            for friend in friends:
                try:
                    obj = TwitterAccount.objects.get(id=friend.id)
                except TwitterAccount.DoesNotExist:
                    TwitterAccount.objects.create(
                        id=friend.id, name=friend.name, screen_name=friend.screen_name
                    )
                else:
                    obj.name = friend.name
                    obj.screen_name = friend.screen_name
                    obj.save()
        return super().get_redirect_url(*args, **kwargs)
