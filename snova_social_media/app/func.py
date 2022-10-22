from api.models import *


def is_post(request):
    return request.method == 'POST'


def get_follower_list(user):
    follows = Follow.objects.all()
    followed_user_list = []
    for f in follows:
        if f.following_user == user:
            followed_user_list.append(f.followed_user)
    return followed_user_list


def get_following_list(user):
    follows = Follow.objects.all()
    following_user_list = []
    for f in follows:
        if f.followed_user == user:
            following_user_list.append(f.following_user)
    return following_user_list


def up_vote_post(user, post):

    pass
