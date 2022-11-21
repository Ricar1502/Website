
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    Model, CharField, ForeignKey, IntegerField, BooleanField)
from django.core.files.storage import FileSystemStorage
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
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

    def __str__(self):

        return f'{self.user}'


class Post(models.Model):
    title = models.CharField(max_length=200, default="")
    content = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=2083, default="", blank=True, null=True)
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    pic = models.ImageField(blank=True, null=True)
    status = models.CharField(max_length=15, default="activate")
    created_at = models.DateTimeField(auto_now_add=True)
    best_score = models.IntegerField(default=0)

    def get_id(self):
        return self.id

    def get_absolute_url(self):
        return "/%i" % self.id

    def __str__(self):
        # print(type(self.parent))

        return f'{self.title}'

    def get_weeks(self):
        return int((timezone.now() - self.created_at).days)//7

    def get_days(self):
        return int((timezone.now() - self.created_at).days)

    def get_hours(self):
        return int(self.get_seconds() // 3600)

    def get_minutes(self):
        return int((self.get_seconds() % 3600) // 60.)

    def get_seconds(self):
        return int((timezone.now() - self.created_at).seconds)


class Vote(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    v_flag = models.BooleanField(null=True, blank=True)
    last_update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.v_flag:
            return f'{self.user_id} upvote for {self.post_id}'
        return f'{self.user_id} downvote for {self.post_id}'


class Rank(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    hot = models.FloatField(default=0)
    new = models.FloatField(default=0)
    raising = models.FloatField(default=0)
    controversial = models.FloatField(default=0)
    top = models.FloatField(default=0)
    best = models.FloatField(default=0)

    def __str__(self):

        return f'rank of: {self.post_id}'


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, default='something')
    content = models.CharField(
        max_length=100000, default="", null=True, blank=True)
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    depth = models.PositiveSmallIntegerField(default=0)
    tree = models.CharField(max_length=200, default="0")
    # children = ArrayField(models.IntegerField(), default=list)

    def get_weeks(self):
        return int((timezone.now() - self.created_at).days)//7

    def get_days(self):
        return int((timezone.now() - self.created_at).days)

    def get_hours(self):
        return int(self.get_seconds() // 3600)

    def get_minutes(self):
        return int((self.get_seconds() % 3600) // 60.)

    def get_seconds(self):
        return int((timezone.now() - self.created_at).seconds)

    class Meta:
        # sort comments in chronological order by default
        ordering = ('created_at',)

    def __str__(self):
        # print(type(self.parent))
        temp = ''
        comment = self
        while comment != None:
            temp = str(comment.id)+'_' + temp
            comment = comment.parent

        return f'{temp}'

    def _calculate_tree(self):
        temp = str(self.content)
        comment = self.parent
        while comment != None:
            temp = str(comment.content)+'_' + temp

            comment = comment.parent
        return temp

    def print_tree(self):
        print(self.content)
        for child in self.children:
            print(child.content)

    def save(self, *args, **kwargs):
        self.tree = self._calculate_tree()
        super(Comment, self).save(*args, **kwargs)


class Follow(models.Model):
    following_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='%(class)s_following')
    followed_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='%(class)s_followed')

    def __str__(self):
        # print(type(self.parent))

        return f'{self.following_user} follow {self.followed_user}'


class Room(models.Model):
    this_profile = models.ForeignKey(
        Profile, related_name='this_profile', on_delete=models.CASCADE)
    selected_profile = models.ForeignKey(
        Profile, related_name='selected_profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    value = models.CharField(max_length=10000)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Notification(models.Model):
    # 1 = Upvote, 2 = Comment, 3 = Follow, 4 = Downvote, 5 = NewPost
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(
        User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(
        User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
