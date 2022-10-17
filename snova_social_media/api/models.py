import email
from django.db import models
# Create your models here.


class User(models.Model):

    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='api/files/avatar')
    email = models.EmailField(max_length=254)
    bio = models.CharField(max_length=200)
    birthday = models.DateField(auto_now_add=False)


class Post(models.Model):
    subreddit_id = models.IntegerField(max_length=50)
    title = models.CharField(max_length=200, default="0")
    content = models.CharField(max_length=200, default="0")
    link = models.CharField(max_length=2083, default="", blank=True, null=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="api/files/post", blank=True, null=True)
    status = models.CharField(max_length=15, default="activate")
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


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, default='something')
    content = models.CharField(max_length=200, default="0")
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    following_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_following')
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_followed')
