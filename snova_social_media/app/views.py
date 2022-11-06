from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .static.python import *
from .func import *
from api.models import Post, Comment, Vote
from .forms import *


# Create your views here.


def home(request):
    posts = Post.objects.all()
    votes = Vote.objects.all()
    for post in posts:
        selected_up_vote = f'upvote-{post.get_id()}'
        selected_down_vote = f'downvote-{post.get_id()}'
        post_id = post
        user_id = post.user_id
        vote(request, selected_up_vote, selected_down_vote,
             post_id, user_id)

    return render(request, 'app/home.html', {'post_list': posts})


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

def login(request):
    result = ''
    return render(request, 'app/login.html', {'result': result})

def register(request):
    result = ''
    return render(request, 'app/register.html', {'result': result})

def create_post_form(request):
    initial_data = {
        "parent_id": '1',
        "type": "post",
    }
    if is_post(request):
        post_form = CreateNewPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            subreddit_id = post_form.cleaned_data['subreddit_id']
            title = post_form.cleaned_data["title"]
            content = post_form.cleaned_data["content"]
            link = post_form.cleaned_data["link"]
            user_id = post_form.cleaned_data["user_id"]
            pic = post_form.cleaned_data["pic"]
            status = post_form.cleaned_data["status"]
            votes = post_form.cleaned_data["votes"]
            t = Post(subreddit_id=subreddit_id, title=title, content=content, link=link, user_id=user_id,
                     pic=pic, status=status, votes=votes)
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

            t = User(name=name, nickname=nickname,
                     password=password, avatar=avatar, email=email, bio=bio, birthday=birthday)
            t.save()
            return HttpResponseRedirect(f"/user/{t.id}")
    else:
        form = CreateNewUserForm()

    return render(request, 'app/createUser.html', {'form': form})


def viewPost(request, id):
    post = Post.objects.get(id=id)
    comment_list = Comment.objects.all()
    return render(request, 'app/viewPost.html', {'post': post, 'comment_list': comment_list})


def view_post_list(request):
    posts = Post.objects.all()
    for i in posts:
        print(i.id)
    return render(request, 'app/viewPostList.html', {'post_list': posts})


def user(request, id):
    user = User.objects.get(id=id)
    comment_list = Comment.objects.all()
    post_list = Post.objects.all()
    follower_list = get_follower_list(user)
    following_list = get_following_list(user)

    return render(request, 'app/viewUser.html', {'user': user, 'follower_list': follower_list, 'following_list': following_list, 'post_list': post_list, 'comment_list': comment_list})


def view_user_list(request):
    user_list = User.objects.all()
    return render(request, 'app/viewUserList.html', {'user_list': user_list})
