import operator
import os
import profile
from itertools import chain

from api.models import Comment, Post, Vote
from django.contrib import messages
from django.contrib.auth import authenticate  # add this
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import *
from .func import *

# Create your views here.


def home(request):
    if (request.user.is_authenticated):
        profile = Profile.objects.get(user = request.user)
        posts = Post.objects.all()  
        follower_list = get_follower_list(profile)
        following_list = get_following_list(profile)
        this_user = request.user
        this_profile = Profile.objects.get(user=this_user)
        votes = get_multiple_post_vote(request, posts)
        context = {'post_list': posts, 'votes': votes, 'profile': this_profile,
                   'follower_list': follower_list, 'following_list': following_list, }
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
        postnotification = Notification.objects.create(notification_type= 5, from_user= user.user, to_user= f.user, post= post)
        postnotification.save()

def viewPost(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post_id=post).order_by('tree')
    votes = get_single_post_vote(request, post)
    if is_post(request):
        current_user = request.user
        current_profile = Profile.objects.get(user=current_user)
        comment_form = CommentForm(data=request.POST, initial={
                                   'user_id': current_profile})
        if comment_form.is_valid():
            comment(request, comment_form, post, current_profile)
            
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    return render(request, 'app/viewPost.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'votes': votes})


def view_user(request, id):
    current_user_profile = Profile.objects.get(user=request.user)
    try:
        profile = Profile.objects.get(id = id)
    except:
        redirect('/user/' + str(current_user_profile.user.id) + '/delete')

    comment_list = Comment.objects.all()
    post_list = Post.objects.all()
    follow(request, id)
    follower_list = get_follower_list(profile)
    following_list = get_following_list(profile)
    votes = get_multiple_post_vote(request, post_list)
    context = {'votes': votes, 'follower_list': follower_list, 'following_list': following_list,
               'post_list': post_list, 'comment_list': comment_list, 'profile': profile, 'current_user_profile': current_user_profile}
    return render(request, 'app/viewUser.html', context)

def view_updateProfile(request, id):
    current_profile = Profile.objects.get(user = request.user)
    try:
        profile = Profile.objects.get(id = id)
    except:
        return HttpResponseRedirect(f"/user/{str(current_profile.user.id + 1)}/profile")
    
    
    if (current_profile.id == id):
        form = UpdateProfile(request.POST, request.FILES)
        context = {'profile' : profile, 'form' : form}
        if is_post(request):
            if form.is_valid():
                avatar = form.cleaned_data["avatar"]
                email = form.cleaned_data["email"]
                bio = form.cleaned_data["bio"]
                up = Profile.objects.filter(user=request.user).update(avatar=avatar, email=email, bio=bio)

            return HttpResponseRedirect(f"/user/{id}")
    else:
        form = UpdateProfile()
        url = '/user/' + str(current_profile.id) + '/profile'
        return redirect(url)

    context = {'profile' : profile, 'form' : form}
    return render(request, 'app/updateprofile.html', context)

def delete_profile(username):
    user = User.objects.get(username=username)
    print(user)
    p = Profile.objects.filter(user=user).delete()
    q = User.objects.filter(username=username).delete()

def delete_notification(user):
    fnotifications = Notification.objects.filter(from_user= user).delete()
    tnotifications = Notification.objects.filter(to_user= user).delete()

def view_deleteProfile(request, id):
    current_profile = Profile.objects.get(user = request.user)
    try:
        profile = Profile.objects.get(id = id)
    except:
        redirect('/user/' + str(current_profile.user.id) + '/delete')

    if(current_profile.id == id):
        context = {'profile' : profile}
        if request.method == "POST":
            username = request.user.username
            delete_profile(username)
            delete_notification(request.user)
            return redirect('/')
    elif(current_profile.id != id):
        url = '/user/' + str(current_profile.id) + '/delete'
        return redirect(url)
    
    return render(request, 'app/deleteprofile.html', {'profile': profile})  

    
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
            messages.success(request, 'success')
            return redirect('/login/')
        else:
            messages = "Thông tin không hợp lệ! Đăng ký thất bại!"
            return render(request, 'app/register.html', {'form': form, 'messages': messages})
    else:
        form = RegisterForm()

    messages = " " 
    return render(request, 'app/register.html', {'form': form, 'messages': messages})


def new_page(request):
    return render(request, 'app/newPage.html')


def best_page(request):
    votes_dict = {}
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


def follow(request, user_id):
    current_user_profile = Profile.objects.get(user=request.user)
    following_user = current_user_profile
    selected_user = Profile.objects.get(id=user_id)
    followed_user = selected_user

    if is_post(request):
        if Follow.objects.filter(following_user=following_user, followed_user=followed_user).first():
            print('this delete')
            delete_follow = Follow.objects.filter(
                following_user=following_user)
            delete_follow.delete()

            delete_notification = Notification.objects.filter(notification_type = 3, from_user = following_user.user, to_user= followed_user.user)
            delete_notification.delete()
            return redirect(f'/user/{user_id}')
        else:
            print('this add')
            new_follow = Follow.objects.create(
                following_user=following_user, followed_user=followed_user)
            new_follow.save()
            new_notification = Notification.objects.create(notification_type = 3, from_user = following_user.user, to_user= followed_user.user)
            new_notification.save()
            return redirect(f'/user/{user_id}')
    else:
        return redirect('/')

def notification_view(request):
    notifications = Notification.objects.filter(to_user= request.user).exclude(user_has_seen=True).order_by('-date')
    print()
    return render(request, 'app/notifications.html', {'notifications' : notifications})