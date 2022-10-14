import email
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class User(models.Model):

    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='files/avatar')
    email = models.EmailField(max_length=254)
    bio = models.CharField(max_length=200)
    birthday = models.DateField(auto_now_add=False)


class Post(models.Model):
    parent_id = models.IntegerField(max_length=50)
    title = models.CharField(max_length=200, default="0")
    content = models.CharField(max_length=200, default="0")
    link = models.CharField(max_length=2083, default="", blank=True, null=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    pic = models.ImageField(upload_to="files/post", blank=True, null=True)
    status = models.CharField(max_length=15, default="activate")
    type = models.CharField(max_length=15, )
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    v_flag = models.BooleanField()
    last_update_time = models.DateTimeField(auto_now_add=True)


class Ranks(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    hot = models.FloatField()
    new = models.FloatField()
    raising = models.FloatField()
    controversial = models.FloatField()
    top = models.FloatField()


# UserModel = get_user_model()
