from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('add/', add),
    path('create_post/', create_post_form),
    path("<int:id>", viewPost),
    path("user/<int:id>", view_user),
    path("search/",  search_view),
    path('logout/', logout_page),
    path("login/",  login_page),
    path("register/",  register_page),
    path("vote/", vote_view),
]
