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
        post_form = CreateNewPostForm()

    return render(request, 'app/createPost.html', {'form': post_form})


def post(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'app/post.html', {'post': post})
