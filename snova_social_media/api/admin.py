from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Ranks)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Follow)
