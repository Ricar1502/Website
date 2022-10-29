from rest_framework import serializers
from .models import Post, Profile, Ranks, Vote


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class RanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranks
        fields = '__all__'


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
