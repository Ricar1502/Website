from api.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


def is_post(request):
    return request.method == 'POST'


def get_random_user(request):
    random_user = []
    all_profile = Profile.objects.all()
    current_profile = Profile.objects.get(user=request.user)
    all_followed = get_follower_list(current_profile)
    for profile in all_profile:
        if profile not in random_user:
            if profile != current_profile:
                if profile not in all_followed:
                    random_user.append(profile)

    return random_user


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


def create_if_vote_dont_exist(data, post_data, user_data, v_flag_data=None):
    if not data.objects.filter(post_id=post_data, user_id=user_data).exists():
        v = Vote(user_id=user_data, post_id=post_data, v_flag=v_flag_data)
        v.save()


def un_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).delete()
    Notification.objects.filter(
        notification_type=1, to_user=user_data.user, post=post_data).delete()
    Notification.objects.filter(
        notification_type=4, to_user=user_data.user, post=post_data).delete()


def up_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=True)
    Notification.objects.create(
        notification_type=1, to_user=user_data.user, post=post_data)


def down_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=False)
    Notification.objects.create(
        notification_type=4, to_user=user_data.user, post=post_data)


def vote(request, selected_up_vote_btn, selected_down_vote_btn, post_id, user_id):
    if selected_up_vote_btn in request.POST:
        create_if_vote_dont_exist(Vote, post_id, user_id)
        current_selected_vote = Vote.objects.get(
            post_id=post_id, user_id=user_id)
        if current_selected_vote.v_flag != True:
            up_vote(Vote, post_id, user_id)
        else:
            un_vote(Vote, post_id, user_id)
    if selected_down_vote_btn in request.POST:
        create_if_vote_dont_exist(Vote, post_id, user_id)
        current_selected_vote = Vote.objects.get(
            post_id=post_id, user_id=user_id)
        if current_selected_vote.v_flag != False:
            down_vote(Vote, post_id, user_id)
        else:
            un_vote(Vote, post_id, user_id)


def comment(request, comment_form, post, current_profile):
    parent_obj = None
    try:
        parent_id = int(request.POST['parent_id'])
    except:
        parent_id = None
    if is_comment_have_parent(parent_id):
        parent_obj = Comment.objects.get(id=parent_id)
        if is_parent_obj_exist(parent_obj):
            replay_comment = comment_form.save(commit=False)
            replay_comment.parent = parent_obj
    save_comment(comment_form, post, current_profile)


def is_comment_have_parent(parent_id):
    return True if parent_id else None


def is_parent_obj_exist(parent_obj):
    return True if parent_obj else None


def save_comment(comment_form, post, current_profile):
    new_comment = comment_form.save(commit=False)
    # assign ship to the comment
    new_comment.post_id = post
    new_comment.user_id = current_profile

    new_comment.depth += 2
    if new_comment.parent:
        new_comment.depth += new_comment.parent.depth
    # new_comment.user_id = current_user
    # save

    new_comment.save()
    user = get_user(post)
    notification = Notification.objects.create(
        notification_type=2, to_user=user, comment=new_comment)


def get_user(post):
    userprofile = post.user_id
    user = userprofile.user

    return user


def get_single_post_vote(request, post):
    vote_list = {}
    current_vote = Vote.objects.filter(post_id=post)
    vote_list[post] = current_vote

    return vote_list


def get_multiple_post_vote(request, posts):
    vote_list = {}
    for post in posts:
        current_vote = Vote.objects.filter(post_id=post)
        vote_list[post] = current_vote
    return vote_list


def voting_on_multiple_post_page(request, posts):
    votes = {}
    for post in posts:
        create_rank_of_post(request, post)
        selected_up_vote_btn = f'upvote-{post.get_id()}'
        selected_down_vote_btn = f'downvote-{post.get_id()}'
        current_vote = Vote.objects.filter(post_id=post)
        votes[post] = current_vote
        post_id = post
        user_id = request.user
        current_profile = Profile.objects.get(user_id=user_id)
        vote(request, selected_up_vote_btn, selected_down_vote_btn,
             post_id, current_profile)
        calculate_best_score(request, post)
        calculate_controversial_score(request, post)


def voting_on_singular_post_page(request, post):
    votes = {}
    selected_up_vote_btn = f'upvote-{post.id}'
    selected_down_vote_btn = f'downvote-{post.id}'
    current_vote = Vote.objects.filter(post_id=post)
    post_id = post
    user_id = request.user
    current_profile = Profile.objects.get(user_id=user_id)
    vote(request, selected_up_vote_btn, selected_down_vote_btn,
         post_id, current_profile)
    calculate_best_score(request, post)
    calculate_controversial_score(request, post)


def calculate_best_score(request, post):
    post_rank = Rank.objects.get(post_id=post)
    upvote_count = 0
    votes = Vote.objects.filter(post_id=post)
    for vote in votes:
        if vote.v_flag:
            upvote_count += 1
    post_rank.best = upvote_count
    post_rank.save()


def calculate_controversial_score(request, post):
    post_rank = Rank.objects.get(post_id=post)
    down_vote_count = 0
    votes = Vote.objects.filter(post_id=post)
    for vote in votes:
        if not vote.v_flag:
            down_vote_count += 1
    post_rank.controversial = down_vote_count
    post_rank.save()


def create_rank_of_post(request, post):
    if Rank.objects.filter(post_id=post).exists():
        return
    rank = Rank(post_id=post)
    rank.save()


def today_time(time):
    return datetime.datetime.today().replace(hour=time.hour, minute=time.minute, second=time.second,
                                             microsecond=time.microsecond, tzinfo=time.tzinfo)


def times_to_delta(start_time, end_time):
    return today_time(end_time) - today_time(start_time)


def send_message(request, user_id):
    message_value = request.GET['message']
    print(message_value)
    print(message_value)
    print(message_value)
    print(message_value)
    print(message_value)
    print(message_value)
    print(message_value)
    return redirect(f'/chat/{user_id}')


def delete_profile(username):
    user = User.objects.get(username=username)
    print(user)
    delete_profile = Profile.objects.filter(user=user).delete()
    delete_user = User.objects.filter(username=username).delete()


def delete_notification(user):
    f_notifications = Notification.objects.filter(from_user=user).delete()
    t_notifications = Notification.objects.filter(to_user=user).delete()


def delete_follow(following_user, followed_user):
    delete_follow = Follow.objects.get(
        following_user=following_user, followed_user=followed_user)
    delete_follow.delete()


def delete_follow_notifications(following_user, followed_user, type=3):
    delete_notification = Notification.objects.filter(
        notification_type=type, from_user=following_user.user, to_user=followed_user.user)
    delete_notification.delete()


def add_follow(following_user, followed_user):
    new_follow = Follow.objects.create(
        following_user=following_user, followed_user=followed_user)
    new_follow.save()


def add_follow_notifications(following_user, followed_user, type=3):
    new_notification = Notification.objects.create(
        notification_type=3, from_user=following_user.user, to_user=followed_user.user)
    new_notification.save()
