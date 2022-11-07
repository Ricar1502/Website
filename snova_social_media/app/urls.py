from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('add/', add),
    path('create_post/', create_post_form),
    path('create_user/', create_user_form),
    path("<int:id>", viewPost),
    path("user/<int:id>", user),
    path("post_list/", view_post_list),
    path("user_list/",  view_user_list),
    path("search/",  search),
    path("login/",  loginPage),
    path("register/",  registerPage),
    path("follow/",  follow),
    path("vote/", vote)
    # path("login/",  login),
    #     path("register/",  register),
]
