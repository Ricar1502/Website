from django.urls import path
from .views import home, add, create_post_form, post, create_user_form, user

urlpatterns = [
    path('', home),
    path('add/', add),
    path('create_post/', create_post_form),
    path('create_user/', create_user_form),
    path("<int:id>", post),
    path("user/<int:id>", user),

]
