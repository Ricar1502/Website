from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer, UserSerializer, RanksSerializer
from .models import Post, User, Ranks
# Create your views here.


class PostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    post1 = Post.objects.get(parent_id='0')
    print(post1.title)


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RanksView(generics.CreateAPIView):
    queryset = Ranks.objects.all()
    serializer_class = RanksSerializer
