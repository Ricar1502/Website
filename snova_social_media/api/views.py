from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer, UserSerializer, RanksSerializer, VotesSerializer, NotificationSerializer
from .models import Post, Profile, Rank, Vote, Notification
# Create your views here.


class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class RanksView(generics.ListAPIView):
    queryset = Rank.objects.all()
    serializer_class = RanksSerializer


class VotesView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VotesSerializer

class NotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serialize_class = NotificationSerializer