from rest_framework import serializers
from .models import Post, User, Ranks, Vote


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'link',
                  'user_id', 'pic', 'status', 'votes', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'password', 'nickname', 'avatar',
                  'email', 'bio', 'birthday')


class RanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranks
        fields = ('post_id', 'hot', 'new', 'raising', 'controversial',
                  'top')


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
