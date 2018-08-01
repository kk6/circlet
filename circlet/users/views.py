# -*- coding: utf-8 -*-
import arrow
import tweepy

from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView

from circlet.middleware import get_api

from .api import create_or_update_twitter_account
from .models import TwitterAccount, UserSettings, Friendship


class TwitterLoginRedirectView(RedirectView):
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.CALLBACK_URL)

    def get_authorization_url(self):
        try:
            url = self.oauth.get_authorization_url()
        except tweepy.TweepError:
            raise tweepy.TweepError("Error! Failed to get request token")
        return url

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.get_authorization_url()
        self.request.session["request_token"] = self.oauth.request_token
        return super().get_redirect_url(*args, **kwargs)


class TwitterCallbackRedirectView(RedirectView):
    pattern_name = "dashboard"
    oauth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    user_model = User

    def get_access_token(self, verifier):
        try:
            self.oauth.get_access_token(verifier)
        except tweepy.TweepError:
            raise tweepy.TweepError("Error! Failed to get access token.")
        return (self.oauth.access_token, self.oauth.access_token_secret)

    def get_or_create_user(self, screen_name):
        try:
            # FIXME: screen_name は変わることがあるのでこれだとマズい。今はとりあえず。
            user = self.user_model.objects.get(username=screen_name)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create_user(username=screen_name)
        return user

    def get_redirect_url(self, *args, **kwargs):
        verifier = self.request.GET.get("oauth_verifier")
        self.oauth.request_token = self.request.session["request_token"]
        token, secret = self.get_access_token(verifier)
        self.request.session["access_token_data"] = {"access_token": token, "access_token_secret": secret}
        api = get_api(token, secret)
        twitter_account = api.me()
        obj = create_or_update_twitter_account(twitter_account.id, twitter_account.name, twitter_account.screen_name)
        user = self.get_or_create_user(twitter_account.screen_name)
        user_settings, _ = UserSettings.objects.get_or_create(user=user)
        user_settings.twitter_account = obj
        user_settings.save()
        return super().get_redirect_url(*args, **kwargs)


def dashboard(request):
    user = request.twitter_api.me()
    friendships = Friendship.objects.filter(user=request.user)
    last_synced_humanized = None
    if friendships.exists():
        friendships_count = friendships.count()
        last_synced = friendships.latest("modified").modified
        last_synced_humanized = arrow.get(last_synced).humanize(locale="ja")
    else:
        friendships_count = 0
        last_synced = None
    return render(request,
                  "dashboard.html",
                  context={"user": user, "friendships_count": friendships_count, "last_synced": last_synced,
                           "last_synced_humanized": last_synced_humanized})


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
                ta = create_or_update_twitter_account(friend.id, friend.name, friend.screen_name)
                try:
                    Friendship.objects.get(user=self.request.user, twitter_account=ta)
                except Friendship.DoesNotExist:
                    friendship = Friendship(user=self.request.user, twitter_account=ta)
                    friendship.save()
        return super().get_redirect_url(*args, **kwargs)
