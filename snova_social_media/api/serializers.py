from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'parent_id', 'title', 'content', 'link',
                  'user_id', 'pic', 'status', 'type', 'votes', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'name', 'password', 'nickname', 'avatar',
                  'email', 'bio', 'birthday')
