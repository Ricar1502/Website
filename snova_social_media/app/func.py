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


def comment(request, comment_form, post, current_user):
    parent_obj = None
    # get parent comment id from hidden input
    try:
        # id integer e.g. 15
        parent_id = int(request.POST['parent_id'])
    except:
        parent_id = None
    # if parent_id has been submitted get parent_obj id
    if check_if_comment_have_parent(parent_id):
        parent_obj = Comment.objects.get(id=parent_id)
        # parent_obj.depth += 5
        # if parent object exist
        if check_if_parent_obj_exist(parent_obj):
            # breakpoint()
            # create replay comment object
            replay_comment = comment_form.save(commit=False)
            # assign parent_obj to replay comment
            replay_comment.parent = parent_obj
    save_comment(comment_form, post, current_user)

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


def check_if_comment_have_parent(parent_id):
    return True if parent_id else None


def check_if_parent_obj_exist(parent_obj):
    return True if parent_obj else None


def save_comment(comment_form, post, current_user):
    new_comment = comment_form.save(commit=False)
    # assign ship to the comment
    new_comment.post_id = post
    new_comment.user_id = current_user
    new_comment.depth += 1
    if new_comment.parent:
        new_comment.depth += new_comment.parent.depth
    # new_comment.user_id = current_user
    # save
    new_comment.save()
