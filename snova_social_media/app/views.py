from .func import *
from .forms import *
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm  # add this
import operator
from django.contrib.auth import login as auth_login
import os
from itertools import chain
from api.models import *
from django.contrib import messages
from django.contrib.auth import authenticate  # add this
from django.contrib.auth import logout
import operator
import datetime
from django.utils import timezone


# Create your views here.


def home(request):
    if (request.user.is_authenticated):
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.all()
        follower_list = get_follower_list(profile)
        following_list = get_following_list(profile)
        this_user = request.user
        this_profile = Profile.objects.get(user=this_user)
        votes = get_multiple_post_vote(request, posts)
        randomUser = get_random_user(request)
        context = {'post_list': posts, 'votes': votes, 'profile': this_profile,
                   'follower_list': follower_list, 'following_list': following_list,
                   'randomuser': randomUser}
        return render(request, 'app/home.html', context)
    else:
        return redirect('/login')


def vote_view(request):
    posts = Post.objects.all()

    if len(posts) > 1:
        voting_on_multiple_post_page(request, posts)
    else:
        create_rank_of_post(request, posts[0])
        voting_on_singular_post_page(request, posts[0])
    return redirect(request.META.get('HTTP_REFERER'))


def add(request):
    result = ''
    if is_post(request):
        num1 = int(request.POST['inp1'])
        num2 = int(request.POST['inp2'])
        result = num1 + num2
    return render(request, 'app/add.html', {'result': result})


def create_post_form(request):
    initial_data = {
        "parent_id": '1',
        "type": "post",
    }
    current_user = request.user
    current_profile = Profile.objects.get(user=current_user)
    if is_post(request):
        post_form = CreateNewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            title = post_form.cleaned_data["title"]
            content = post_form.cleaned_data["content"]
            link = post_form.cleaned_data["link"]
            pic = post_form.cleaned_data["pic"]
            t = Post(title=title, content=content, link=link, user_id=current_profile,
                     pic=pic)
            t.save()
            Post_notifications(current_profile, t)
            return HttpResponseRedirect(f"/{t.id}")
    else:
        post_form = CreateNewPostForm(initial=initial_data)

    return render(request, 'app/createPost.html', {'form': post_form})


def Post_notifications(user, post):
    follow = get_following_list(user)
    for f in follow:
        post_notification = Notification.objects.create(
            notification_type=5, from_user=user.user, to_user=f.user, post=post)
        post_notification.save()


def viewPost(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post_id=post).order_by('tree')
    votes = get_single_post_vote(request, post)
    current_profile = Profile.objects.get(user=request.user)
    if is_post(request):
        comment_form = CommentForm(data=request.POST, initial={
                                   'user_id': current_profile})
        if comment_form.is_valid():
            comment(request, comment_form, post, current_profile)

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    return render(request, 'app/viewPost.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'votes': votes, 'profile': current_profile})


def view_updatePost(request, id):
    post = Post.objects.get(id=id)
    current_profile = Profile.objects.get(user=request.user)
    if (post.user_id == current_profile):
        form = UpdatePost(request.POST, request.FILES)
        context = {'post': post, 'form': form}
        if is_post(request):
            if form.is_valid():
                print(post, current_profile)
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                pic = form.cleaned_data["pic"]
                up = Post.objects.filter(id=id).update(
                    title=title, content=content, pic=pic)

                return HttpResponseRedirect(f"/{id}")
    else:
        form = UpdatePost()
        return redirect('/')

    context = {'post': post, 'form': form}
    return render(request, 'app/updatepost.html', context)


def view_deletePost(request, id):
    post = Post.objects.get(id=id)
    current_profile = Profile.objects.get(user=request.user)
    if (post.user_id == current_profile):
        context = {'post': post}
        if request.method == "POST":
            delete = Post.objects.filter(id=id).delete()
            return redirect('/')
    else:
        return redirect('/')

    return render(request, 'app/deletepost.html', context)


def view_user(request, id):
    current_user_profile = Profile.objects.get(user=request.user)
    try:
        profile = Profile.objects.get(id=id)
    except:
        redirect('/user/' + str(current_user_profile.user.id) + '/delete')

    comment_list = Comment.objects.all()
    post_list = Post.objects.filter(user_id=profile)
    follow(request, id)
    follower_list = get_follower_list(profile)
    following_list = get_following_list(profile)
    votes = get_multiple_post_vote(request, post_list)
    context = {'votes': votes, 'follower_list': follower_list, 'following_list': following_list,
               'post_list': post_list, 'comment_list': comment_list, 'profile': profile, 'current_user_profile': current_user_profile}
    return render(request, 'app/viewUser.html', context)


def view_updateProfile(request, id):
    current_profile = Profile.objects.get(user=request.user)
    try:
        profile = Profile.objects.get(id=id)
    except:
        return HttpResponseRedirect(f"/user/{str(current_profile.user.id + 1)}/profile")

    if (current_profile.id == id):
        form = UpdateProfile(request.POST, request.FILES)
        context = {'profile': profile, 'form': form}
        if is_post(request):
            if form.is_valid():
                avatar = form.cleaned_data["avatar"]
                email = form.cleaned_data["email"]
                bio = form.cleaned_data["bio"]
                up = Profile.objects.filter(user=request.user).update(
                    avatar=avatar, email=email, bio=bio)

            return HttpResponseRedirect(f"/user/{id}")
    else:
        form = UpdateProfile()
        url = '/user/' + str(current_profile.id) + '/profile'
        return redirect(url)

    context = {'profile': profile, 'form': form}
    return render(request, 'app/updateprofile.html', context)


def delete_profile(username):
    user = User.objects.get(username=username)
    print(user)
    p = Profile.objects.filter(user=user).delete()
    q = User.objects.filter(username=username).delete()


def delete_notification(user):
    f_notifications = Notification.objects.filter(from_user=user).delete()
    t_notifications = Notification.objects.filter(to_user=user).delete()


def view_deleteProfile(request, id):
    current_profile = Profile.objects.get(user=request.user)
    try:
        profile = Profile.objects.get(id=id)
    except:
        redirect('/user/' + str(current_profile.user.id) + '/delete')

    if (current_profile.id == id):
        context = {'profile': profile}
        if request.method == "POST":
            username = request.user.username
            delete_profile(username)
            delete_notification(request.user)
            return redirect('/')
    elif (current_profile.id != id):
        url = '/user/' + str(current_profile.id) + '/delete'
        return redirect(url)

    return render(request, 'app/deleteprofile.html', {'profile': profile})


def search_view(request):
    this_user = request.user
    this_profile = Profile.objects.get(user=this_user)
    username_profile_list = []
    follower_list = {}
    following_list = {}
    username = request.GET['username']
    user_object = Profile.objects.filter(
        user__username__icontains=username)
    for user in user_object:
        username_profile_list.append(user)
        follower = Follow.objects.filter(
            followed_user=user)
        follower_list[user] = follower
        following = Follow.objects.filter(
            following_user=user)
        following_list[user] = following

    context = {'user_profile_list': username_profile_list,
               'following_list': following_list, 'follower_list': follower_list, 'this_profile': this_profile}
    return render(request, 'app/search.html', context)


def logout_page(request):
    logout(request)
    return redirect('/')


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print('username', username, 'password', password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect("/")
            else:
                messages = "Sai username hoặc password! Đăng nhập thất bại!"
                return render(request, 'app/login.html', {'form': form, 'messages': messages})
        else:
            messages = "Sai username hoặc password! Đăng nhập thất bại!"
            return render(request, 'app/login.html', {'form': form, 'messages': messages})
    else:
        form = LoginForm()
    messages = " "
    return render(request, 'app/login.html', {'form': form, 'messages': messages})


def create_profile(username, email):
    user = User.objects.get(username=username)
    print(user)
    p = Profile.objects.create(user=user, email=email)
    p.save()


def register_page(request):
    if is_post(request):
        form = RegisterForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        if form.is_valid():
            form.save()
            create_profile(username, email)
            return redirect('/login/')
        else:
            messages = "Thông tin không hợp lệ! Đăng ký thất bại!"
            return render(request, 'app/register.html', {'form': form, 'messages': messages})
    else:
        form = RegisterForm()

    messages = " "
    return render(request, 'app/register.html', {'form': form, 'messages': messages})


def new_page(request):
    ranks = Rank.objects.all().order_by('-best')
    posts = Post.objects.all().order_by('-created_at')
    votes = get_multiple_post_vote(request, posts)
    profile = Profile.objects.get(user=request.user)

    context = {'ranks': ranks, 'votes': votes,
               'posts': posts, 'profile': profile}

    return render(request, 'app/newPage.html', context)


def best_page(request):
    ranks = Rank.objects.all().order_by('-best')
    posts = Post.objects.all()
    votes = get_multiple_post_vote(request, posts)
    profile = Profile.objects.get(user=request.user)

    context = {'ranks': ranks, 'votes': votes, 'profile': profile}
    return render(request, 'app/bestPage.html', context)


def controversial_page(request):
    votes_dict = {}
    ranks = Rank.objects.all().order_by('-controversial')
    posts = Post.objects.all()
    votes = get_multiple_post_vote(request, posts)
    profile = Profile.objects.get(user=request.user)

    context = {'ranks': ranks, 'votes': votes, 'profile': profile}
    return render(request, 'app/bestPage.html', context)


def follow(request, id):
    current_user_profile = Profile.objects.get(user=request.user)
    following_user = current_user_profile
    selected_user = Profile.objects.get(id=id)
    followed_user = selected_user

    if is_post(request):
        if Follow.objects.filter(following_user=following_user, followed_user=followed_user).first():
            print('this delete')
            delete_follow(following_user)
            delete_follow_notifications(following_user, followed_user)
            return redirect(request.META['HTTP_REFERER'])
        else:
            print('this add')
            add_follow(following_user, followed_user)
            add_follow_notifications(following_user, followed_user)
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('/')


def chat_page(request, id):
    this_user = request.user
    this_profile = Profile.objects.get(user=this_user)
    rooms = Room.objects.all()
    selected_room = Room.objects.get(id=id)
    messages = Messages.objects.filter(room=selected_room)
    send_message(request, id)
    if messages:
        latest_message = messages.latest('created_at')

    else:
        latest_message = ''
    get_all_messages = Messages.objects.filter()
    message_dict = {}
    message_time_dict = {}
    get_all_message_in_room = Messages.objects.filter(room=selected_room)
    print(get_all_message_in_room)
    print(get_all_message_in_room)
    print(get_all_message_in_room)
    print(get_all_message_in_room)
    print(get_all_message_in_room)
    for message in get_all_messages:
        message_dict[message.room] = message.value
        message_time_dict[message.room] = message

    context = {'rooms': rooms,
               'selected_room': selected_room, 'messages': messages, 'this_profile': this_profile, 'latest_message': latest_message, 'message_dict': message_dict, 'message_time_dict': message_time_dict,'get_all_message_in_room':get_all_message_in_room}
    return render(request, 'app/chatPage.html', context)


def send_message(request, id):
    if is_post(request):
        user = request.user
        this_profile = Profile.objects.get(user_id=user)
        message_value = request.POST['message']
        this_room = Room.objects.get(id=id)
        new_message = Messages(value=message_value,
                               profile=this_profile, room=this_room)
        new_message.save()
    return redirect(request.META['HTTP_REFERER'])


def direct_to_first_chat(request):
    this_user = request.user
    this_profile = Profile.objects.get(user=this_user)
    this_user_rooms = Room.objects.filter(this_profile=this_profile).first()
    print(f'this user room is {this_user_rooms}')
    selected_user_rooms = Room.objects.filter(
        selected_profile=this_profile).first()
    print(f'selected user room is {selected_user_rooms}')
    if selected_user_rooms:
        return redirect(f'/chat/{selected_user_rooms.id}')
    else:
        return redirect(f'/chat/{this_user_rooms.id}')


def notification_view(request):
    notifications = Notification.objects.filter(
        to_user=request.user).order_by('-date')
    print()
    return render(request, 'app/notifications.html', {'notifications': notifications})


def followers_view(request, id):
    if (request.user.is_authenticated):
        this_profile = Profile.objects.get(id=id)
        follower_list = get_following_list(this_profile)
        if len(follower_list) == 0:
            context = {'follower_list': follower_list,
                       'this_profile': this_profile, 'message': "No one follows you"}
        else:
            context = {'follower_list': follower_list,
                       'this_profile': this_profile, 'message': " "}
        return render(request, 'app/follower.html', context)
    else:
        return redirect('/login')


def followings_view(request, id):
    if (request.user.is_authenticated):
        this_profile = Profile.objects.get(id=id)
        following_list = get_follower_list(this_profile)
        if len(following_list) == 0:
            context = {'following_list': following_list,
                       'this_profile': this_profile, 'message': "You haven't follow anyone"}
        else:
            context = {'following_list': following_list,
                       'this_profile': this_profile, 'message': " "}
        return render(request, 'app/following.html', context)
    else:
        return redirect('/login')


def chat_redirect(request, id):
    user = request.user
    this_profile = Profile.objects.get(user=user)
    selected_profile = Profile.objects.get(id=id)
    get_all_this_profile_rooms = Room.objects.filter(this_profile=this_profile)
    get_all_selected_profile_rooms = Room.objects.filter(
        selected_profile=this_profile)

    if is_post(request):
        if get_all_this_profile_rooms:
            this_room_exist = Room.objects.filter(
                this_profile=this_profile, selected_profile=selected_profile).exists()
            for room in get_all_this_profile_rooms:
                if this_room_exist:
                    return redirect(f'/chat/{room.id}')
                else:
                    new_room = Room(this_profile=this_profile,
                                    selected_profile=selected_profile)
                    new_room.save()
                    return redirect(f'/chat/{new_room.id}')
        elif get_all_selected_profile_rooms:
            this_room_exist = Room.objects.filter(
                this_profile=selected_profile, selected_profile=this_profile).exists()
            for room in get_all_selected_profile_rooms:
                if this_room_exist:
                    return redirect(f'/chat/{room.id}')
                else:
                    new_room = Room(this_profile=this_profile,
                                    selected_profile=selected_profile)
                    new_room.save()
                    return redirect(f'/chat/{new_room.id}')
        else:
            new_room = Room(this_profile=this_profile,
                            selected_profile=selected_profile)
            new_room.save()
            return redirect(f'/chat/{new_room.id}')
        return redirect('/')


def follow_in_search(request, id):

    this_user = request.user
    this_profile = Profile.objects.get(user=this_user)
    btn_click = request.GET['follow']
    selected_profile = Profile.objects.get(id=id)
    if Follow.objects.filter(following_user=this_profile, followed_user=selected_profile).first():
        print('this delete')
        delete_follow(this_profile, selected_profile)
        delete_follow_notifications(this_profile, selected_profile)
        return redirect(request.META['HTTP_REFERER'])
    else:
        print('this add')
        add_follow(this_profile, selected_profile)
        add_follow_notifications(this_profile, selected_profile)
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/')


def follow_view(request, id):

    this_user = request.user
    this_profile = Profile.objects.get(user=this_user)
    btn_click = request.GET['follow']
    selected_profile = Profile.objects.get(id=id)
    if Follow.objects.filter(following_user=this_profile, followed_user=selected_profile).first():
        print('this delete')
        delete_follow(this_profile, selected_profile)
        delete_follow_notifications(this_profile, selected_profile)
        return redirect(request.META['HTTP_REFERER'])
    else:
        print('this add')
        add_follow(this_profile, selected_profile)
        add_follow_notifications(this_profile, selected_profile)
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/')
