# -*- coding: utf-8 -*-
import arrow
import tweepy
from more_itertools import chunked

from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView

from circlet.middleware import get_api

from .api import create_or_update_twitter_account
from .models import TwitterAccount, UserSettings, Friendship


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
    obj = create_or_update_twitter_account(twitter_account.id, twitter_account.name, twitter_account.screen_name)
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
    twitter_user_info = request.twitter_api.me()
    user_settings = UserSettings.objects.get(twitter_account__id=twitter_user_info.id)
    friendships = Friendship.objects.filter(user=user_settings.user)
    if friendships.exists():
        friendships_count = friendships.count()
        last_synced = friendships.latest("modified").modified
        last_synced_humanized = arrow.get(last_synced).humanize(locale="ja")
    else:
        friendships_count = 0
        last_synced = None
        last_synced_humanized = None
    return render(request,
                  "dashboard.html",
                  context={"twitter_user_info": twitter_user_info, "friendships_count": friendships_count,
                           "last_synced": last_synced, "last_synced_humanized": last_synced_humanized})


class FetchTwitterFollowingsRedirectView(RedirectView):
    pattern_name = "dashboard"

    def get_redirect_url(self, *args, **kwargs):
        # TODO: フォロー外れた人のFriendshipレコードが残ったままとなり、twitter上のフォロー数より多くなる問題を直す
        api = self.request.twitter_api
        twitter_user_info = api.me()
        user_settings = UserSettings.objects.get(twitter_account__id=twitter_user_info.id)
        friends_ids = api.friends_ids(twitter_user_info.id)
        chunked_friends_ids = chunked(friends_ids, 100)
        for friends_ids in chunked_friends_ids:
            friends = api.lookup_users(user_ids=friends_ids)
            for friend in friends:
                ta = create_or_update_twitter_account(friend.id, friend.name, friend.screen_name)
                try:
                    Friendship.objects.get(user=user_settings.user, twitter_account=ta)
                except Friendship.DoesNotExist:
                    friendship = Friendship(user=user_settings.user, twitter_account=ta)
                    friendship.save()
        return super().get_redirect_url(*args, **kwargs)
