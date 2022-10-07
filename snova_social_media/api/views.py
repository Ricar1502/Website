from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer, UserSerializer
from .models import Post, User
# Create your views here.


class PostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    post1 = Post.objects.get(parent_id='0')
    print(post1.title)


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
