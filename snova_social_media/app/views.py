import profile
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .func import *
from api.models import Post, Comment, Vote
from .forms import *
from itertools import chain
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
# Create your views here.


def home(request):
    posts = Post.objects.all()
    votes = {}
    for post in posts:
        selected_up_vote_btn = f'upvote-{post.get_id()}'
        selected_down_vote_btn = f'downvote-{post.get_id()}'
        current_vote = Vote.objects.filter(post_id=post)
        votes[post] = current_vote
        post_id = post
        user_id = request.user
        vote(request, selected_up_vote_btn, selected_down_vote_btn,
             post_id, user_id)

    print(request.user)
    return render(request, 'app/home.html', {'post_list': posts, 'votes': votes})


# def vote(request):
#     if is_post(request):
#         if 'upvote' in request.POST:
#             upvote = request.POST['upvote']
#             print('this is upvote')
#         else:
#             upvote = False
#         if 'downvote' in request.POST:
#             downvote = request.POST['downvote']
#         else:
#             downvote = False
#     return render(request, 'app/home.html')


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
    if is_post(request):
        post_form = CreateNewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            title = post_form.cleaned_data["title"]
            content = post_form.cleaned_data["content"]
            link = post_form.cleaned_data["link"]
            user_id = post_form.cleaned_data["user_id"]
            pic = post_form.cleaned_data["pic"]
            status = post_form.cleaned_data["status"]
            t = Post(title=title, content=content, link=link, user_id=user_id,
                     pic=pic, status=status)
            t.save()
            return HttpResponseRedirect(f"/{t.id}")
    else:
        post_form = CreateNewPostForm(initial=initial_data)

    return render(request, 'app/createPost.html', {'form': post_form}
                  )


def create_user_form(request):
    if is_post(request):
        form = CreateNewUserForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            nickname = form.cleaned_data["nickname"]
            password = form.cleaned_data["password"]
            avatar = form.cleaned_data["avatar"]
            email = form.cleaned_data["email"]
            bio = form.cleaned_data["bio"]
            birthday = form.cleaned_data["birthday"]

            t = User.objects.create_user(name=name, nickname=nickname,
                                         password=password, avatar=avatar, email=email, bio=bio, birthday=birthday)
            t.save()
            return HttpResponseRedirect(f"/user/{t.id}")
    else:
        form = CreateNewUserForm()

    return render(request, 'app/createUser.html', {'form': form})


def viewPost(request, id):
    post = Post.objects.get(id=id)
    print(post.pic)
    comment_list = Comment.objects.all()
    user = request.user

    return render(request, 'app/viewPost.html', {'post': post, 'comment_list': comment_list, 'user': user})


def view_post_list(request):
    posts = Post.objects.all()
    for i in posts:
        print(i.id)
    return render(request, 'app/viewPostList.html', {'post_list': posts})


def user(request, id):
    profile = Profile.objects.get(id=id)
    comment_list = Comment.objects.all()
    post_list = Post.objects.all()
    follower_list = get_follower_list(profile)
    following_list = get_following_list(profile)
    print(follower_list)
    print(following_list)
    context = {'follower_list': follower_list, 'following_list': following_list,
               'post_list': post_list, 'comment_list': comment_list, 'profile': profile}
    return render(request, 'app/viewUser.html', context)


def view_user_list(request):
    user_list = Profile.objects.all()
    return render(request, 'app/viewUserList.html', {'user_list': user_list})


def search(request):

    username_profile_list = []
    follower_list = {}
    following_list = {}
    if is_post(request):
        username = request.POST['username']
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


def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print('username', username, 'password', password)
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="app/login.html", context={"form": form})


def registerPage(request):

    if is_post(request):
        form = UserCreationForm(request.POST)
        print('hi')
        if form.is_valid():
            form.save()

            messages.success(request, 'success')
    else:
        form = UserCreationForm()

    return render(request, 'app/register.html', {'form': form})


def follow(request):
    following_user = request.user
    followed_user = request.POST['user']
    print('hello world')
    # print('following user: %s' % following_user)
    # print('followed user: %s' % followed_user)
    if is_post(request):
        if Follow.objects.filter(following_user=following_user, followed_user=followed_user).first():
            delete_follow = Follow.objects.filter(
                following_user=following_user)
            delete_follow.delete()
            return redirect(f'/user')

        else:
            new_follow = Follow.objects.create(
                following_user=following_user, followed_user=followed_user)

    else:
        return redirect('/')
