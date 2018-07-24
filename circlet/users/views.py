# -*- coding: utf-8 -*-
import tweepy

from django.shortcuts import redirect, render
from django.conf import settings


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