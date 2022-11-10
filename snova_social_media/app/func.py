from api.models import *
from django.http import HttpResponse, HttpResponseRedirect


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


def create_if_vote_dont_exist(data, post_data, user_data, v_flag_data=None):
    if not data.objects.filter(post_id=post_data, user_id=user_data).exists():
        v = Vote(user_id=user_data, post_id=post_data, v_flag=v_flag_data)
        v.save()


def un_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).delete()


def up_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=True)


def down_vote(data, post_data, user_data):
    data.objects.filter(
        post_id=post_data, user_id=user_data).update(v_flag=False)


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

    # # normal comment
    # # create comment object but do not save to database
    # new_comment = comment_form.save(commit=False)
    # # assign ship to the comment
    # new_comment.post_id = post
    # new_comment.user_id = current_user
    # new_comment.depth += 1
    # if new_comment.parent:
    #     new_comment.depth += new_comment.parent.depth
    # # new_comment.user_id = current_user
    # # save
    # new_comment.save()
    # comment_list = Comment.objects.all()


def is_comment_have_parent(parent_id):
    return True if parent_id else None


def is_parent_obj_exist(parent_obj):
    return True if parent_obj else None


def save_comment(comment_form, post, current_profile):
    new_comment = comment_form.save(commit=False)
    # assign ship to the comment
    new_comment.post_id = post
    new_comment.user_id = current_profile

    new_comment.depth += 1
    if new_comment.parent:
        new_comment.depth += new_comment.parent.depth
    # new_comment.user_id = current_user
    # save
    new_comment.save()


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
        selected_up_vote_btn = f'upvote-{post.get_id()}'
        selected_down_vote_btn = f'downvote-{post.get_id()}'
        current_vote = Vote.objects.filter(post_id=post)
        votes[post] = current_vote
        post_id = post
        user_id = request.user
        current_profile = Profile.objects.get(user_id=user_id)
        vote(request, selected_up_vote_btn, selected_down_vote_btn,
             post_id, current_profile)


def voting_on_singular_post_page(request, post):
    votes = {}
    selected_up_vote_btn = f'upvote-{post.get_id()}'
    selected_down_vote_btn = f'downvote-{post.get_id()}'
    current_vote = Vote.objects.filter(post_id=post)
    post_id = post
    user_id = request.user
    current_profile = Profile.objects.get(user_id=user_id)
    vote(request, selected_up_vote_btn, selected_down_vote_btn,
         post_id, current_profile)
