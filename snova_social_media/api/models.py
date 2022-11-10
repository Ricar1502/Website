
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

    def get_absolute_url(self):
        return "/%i" % self.id


class Vote(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
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
    content = models.CharField(max_length=200, default="")
    user_id = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    depth = models.PositiveSmallIntegerField(default=0)
    tree = models.CharField(max_length=200, default="0")
    # children = ArrayField(models.IntegerField(), default=list)

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


# class SubNova(models.Model):
#     user_id = models.ForeignKey(
#         User, on_delete=models.CASCADE)
#     post_id = models.ForeignKey(
#         Post, on_delete=models.CASCADE, default='something')
#     pic = models.ImageField(upload_to="api/files/post", blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    # User, on_delete=models.CASCADE, related_name='%(class)s_followed')
