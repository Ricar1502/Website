from django.contrib import admin
from .models import Post, User, Ranks
# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Ranks)
