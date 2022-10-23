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


def test():
    print("Testing")


def create_if_vote_dont_exist(data, post_data, user_data, v_flag_data=None):
    if not data.objects.filter(post_id=post_data, user_id=user_data).exists():

        v = Vote(user_id=user_data, post_id=post_data, v_flag=v_flag_data)
        v.save()


def un_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=None)


def up_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=True)


def down_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=False)


def vote(request, selected_up_vote, selected_down_vote, post_id, user_id):
    if selected_up_vote in request.POST:
        create_if_vote_dont_exist(Vote, post_id, user_id)
        current_selected_vote = Vote.objects.get(
            post_id=post_id, user_id=user_id)
        f = current_selected_vote.v_flag
        if current_selected_vote.v_flag != True:
            up_vote(Vote, post_id, user_id)
        else:
            un_vote(Vote, post_id, user_id)
    if selected_down_vote in request.POST:
        create_if_vote_dont_exist(Vote, post_id, user_id)
        current_selected_vote = Vote.objects.get(
            post_id=post_id, user_id=user_id)
        if current_selected_vote.v_flag != False:
            down_vote(Vote, post_id, user_id)
        else:
            un_vote(Vote, post_id, user_id)
