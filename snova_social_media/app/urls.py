from django.urls import path
from .views import home, add, create_post_form, viewPost, create_user_form, user, viewPostList

urlpatterns = [
    path('', home),
    path('add/', add),
    path('create_post/', create_post_form),
    path('create_user/', create_user_form),
    path("<int:id>", viewPost),
    path("user/<int:id>", user),
    path("post_list/", viewPostList),

]
