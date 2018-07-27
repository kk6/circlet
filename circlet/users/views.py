# -*- coding: utf-8 -*-
import tweepy

from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic.base import RedirectView

from .models import TwitterAccount


def login(request):
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,
                               settings.CONSUMER_SECRET,
                               settings.CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise tweepy.TweepError('Error! Failed to get request token')
    request.session['request_token'] = auth.request_token
    return redirect(redirect_url)


def callback(request):
    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,
                               settings.CONSUMER_SECRET)
    auth.request_token = request.session['request_token']
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
    request.session['access_token_data'] = {
        'access_token': auth.access_token,
        'access_token_secret': auth.access_token_secret,
    }
    return redirect('dashboard')


def dashboard(request):
    user = request.twitter_api.me()
    return render(request, 'dashboard.html', context={'user': user})


class FetchTwitterFollowingsRedirectView(RedirectView):
    pattern_name = "dashboard"

    def get_redirect_url(self, *args, **kwargs):
        def chunked(ls, size):
            return [ls[x:x + size] for x in range(0, len(ls), size)]

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
                        id=friend.id,
                        name=friend.name,
                        screen_name=friend.screen_name,
                    )
                else:
                    obj.name = friend.name
                    obj.screen_name = friend.screen_name
                    obj.save()
        return super().get_redirect_url(*args, **kwargs)
