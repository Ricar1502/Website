import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .func import *
from api.models import Post, Comment, Vote
from .forms import *
from itertools import chain
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import authenticate  # add this
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
import os
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
            return HttpResponseRedirect(f"/{t.id}")
    else:
        post_form = CreateNewPostForm(initial=initial_data)

    return render(request, 'app/createPost.html', {'form': post_form})


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


def view_user(request, id):
    profile = Profile.objects.get(id=id)
    current_user_profile = Profile.objects.get(user=request.user)
    comment_list = Comment.objects.all()
    post_list = Post.objects.all()
    follow(request, id)
    follower_list = get_follower_list(profile)
    following_list = get_following_list(profile)
    votes = get_multiple_post_vote(request, post_list)
    context = {'votes': votes, 'follower_list': follower_list, 'following_list': following_list,
               'post_list': post_list, 'comment_list': comment_list, 'profile': profile, 'current_user_profile': current_user_profile}
    return render(request, 'app/viewUser.html', context)


def search_view(request):
    username_profile_list = []
    follower_list = {}
    following_list = {}
    username = request.GET['username']
    user_object = Profile.objects.filter(
        user__username__icontains=username)
    print(user_object)
    for user in user_object:
        username_profile_list.append(user)
        follower = Follow.objects.filter(
            followed_user=user)
        follower_list[user] = follower
        following = Follow.objects.filter(
            following_user=user)
        following_list[user] = following
    context = {'username_profile_list': username_profile_list,
               'following_list': following_list, 'follower_list': follower_list}
    return render(request, 'app/search.html', context)


def logout_page(request):
    logout(request)
    return redirect('/')


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print('username', username, 'password', password)
            print(user)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="app/login.html", context={"form": form})


def create_profile(username):
    user = User.objects.get(username=username)
    print(user)
    p = Profile.objects.create(user=user)
    p.save()


def register_page(request):
    if is_post(request):
        form = UserCreationForm(request.POST)
        username = request.POST['username']
        if form.is_valid():
            form.save()
            create_profile(username)
            messages.success(request, 'success')
    else:
        form = UserCreationForm()

    return render(request, 'app/register.html', {'form': form})


def new_page(request):
    ranks = Rank.objects.all().order_by('-best')
    posts = Post.objects.all().order_by('-created_at')
    votes = get_multiple_post_vote(request, posts)

    context = {'ranks': ranks, 'votes': votes, 'posts': posts}

    return render(request, 'app/newPage.html', context)


def best_page(request):
    ranks = Rank.objects.all().order_by('-best')
    posts = Post.objects.all()
    votes = get_multiple_post_vote(request, posts)

    context = {'ranks': ranks, 'votes': votes}
    return render(request, 'app/bestPage.html', context)


def controversial_page(request):
    votes_dict = {}
    ranks = Rank.objects.all().order_by('-controversial')
    posts = Post.objects.all()
    votes = get_multiple_post_vote(request, posts)

    context = {'ranks': ranks, 'votes': votes}
    return render(request, 'app/bestPage.html', context)


def follow(request, id):
    current_user_profile = Profile.objects.get(user=request.user)
    following_user = current_user_profile
    selected_user = Profile.objects.get(id=id)
    followed_user = selected_user
    if is_post(request):
        if Follow.objects.filter(following_user=following_user, followed_user=followed_user).first():
            print('this delete')
            delete_follow = Follow.objects.filter(
                following_user=following_user)
            delete_follow.delete()
            return redirect(request.META['HTTP_REFERER'])
        else:
            print('this add')
            new_follow = Follow.objects.create(
                following_user=following_user, followed_user=followed_user)
            new_follow.save()
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
    context = {'rooms': rooms,
               'selected_room': selected_room, 'messages': messages, 'this_profile': this_profile}
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
    return redirect(f'/chat/{id}')


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

def followers(request):
    if (request.user.is_authenticated):
        profile = Profile.objects.get(user=request.user)
        follower_list = get_following_list(profile)
        return render(request, 'app/follower.html')
    else:
        return redirect('/login')

def followings(request):
    if (request.user.is_authenticated):
        profile = Profile.objects.get(user=request.user)
        following_list = get_follower_list(profile)
        return render(request, 'app/following.html')
    else:
        return redirect('/login')