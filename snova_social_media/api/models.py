
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    Model, CharField, ForeignKey, IntegerField, BooleanField)
from django.core.files.storage import FileSystemStorage
# Create your models here.

fs = FileSystemStorage()
avatar = fs.url('../default_img.png')


class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, default=avatar)
    email = models.EmailField(max_length=254, blank=True)
    bio = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=200, default="0")
    content = models.CharField(max_length=200, default="0")
    link = models.CharField(max_length=2083, default="", blank=True, null=True)
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    pic = models.ImageField(blank=True, null=True)
    status = models.CharField(max_length=15, default="activate")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_id(self):
        return self.id


class Vote(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    v_flag = models.BooleanField(null=True, blank=True)
    last_update_time = models.DateTimeField(auto_now_add=True)


class Ranks(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    hot = models.FloatField()
    new = models.FloatField()
    raising = models.FloatField()
    controversial = models.FloatField()
    top = models.FloatField()


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, default='something')
    content = models.CharField(max_length=200, default="0")
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    following_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='%(class)s_following')
    followed_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='%(class)s_followed')


# class SubNova(models.Model):
#     user_id = models.ForeignKey(
#         User, on_delete=models.CASCADE)
#     post_id = models.ForeignKey(
#         Post, on_delete=models.CASCADE, default='something')
#     pic = models.ImageField(upload_to="api/files/post", blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    # User, on_delete=models.CASCADE, related_name='%(class)s_followed')
