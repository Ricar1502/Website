from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .static.python import *
from .func import *
from api.models import Post
from .forms import *


# Create your views here.


def home(request):
    return render(request, 'app/base.html')


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
        post_form = CreateNewPostForm(request.POST)
        if post_form.is_valid():
            parent_id = post_form.cleaned_data['parent_id']
            title = post_form.cleaned_data["title"]
            content = post_form.cleaned_data["content"]
            link = post_form.cleaned_data["link"]
            user_id = post_form.cleaned_data["user_id"]
            pic = post_form.cleaned_data["pic"]
            status = post_form.cleaned_data["status"]
            type = post_form.cleaned_data["type"]
            votes = post_form.cleaned_data["votes"]

            t = Post(parent_id=parent_id, title=title, content=content, link=link, user_id=user_id,
                     pic=pic, status=status, type=type, votes=votes)
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


def post(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'app/viewPost.html', {'post': post})


def user(request, id):
    user = User.objects.get(id=id)
    return render(request, 'app/viewUser.html', {'user': user})
