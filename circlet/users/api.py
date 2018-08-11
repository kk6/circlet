# -*- coding: utf-8 -*-
from .models import TwitterAccount, UserSettings, Friendship


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


def get_user_by_twitter_id(twitter_id):
    """Get User by twitter's ID

    :param twitter_id: twitter's user ID.
    :return: User instance.

    """
    settings = UserSettings.objects.get(twitter_account__id=twitter_id)
    return settings.user


def get_removed_followings_ids(user, twitter_friends_ids):
    """Get removed followings's twitter ids.

    :param twitter_friends_ids:
    :return: removed followings's twitter ids.

    """
    circlet_friends_ids = Friendship.objects.filter(user=user).values_list(
        "twitter_account__id", flat=True
    )
    removed_ids = set(circlet_friends_ids).difference(twitter_friends_ids)
    return removed_ids
