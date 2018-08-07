# -*- coding: utf-8 -*-
import tweepy
from django.conf import settings


def get_api(access_token, access_token_secret):
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)
