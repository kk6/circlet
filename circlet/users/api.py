# -*- coding: utf-8 -*-
from .models import TwitterAccount


def create_or_update_twitter_account(twitter_id, name, screen_name):
    """Create or Update TwitterAccount

    :param twitter_id: twitter's user ID.
    :param name: twitter's user name
    :param screen_name: twitter's user screen_name
    :return: TwitterAccount instance

    """
    try:
        obj = TwitterAccount.objects.get(id=twitter_id)
    except TwitterAccount.DoesNotExist:
        obj = TwitterAccount.objects.create(
            id=twitter_id, name=name, screen_name=screen_name
        )
    else:
        obj.name = name
        obj.screen_name = screen_name
        obj.save()
    return obj