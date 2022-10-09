from django.urls import path
from .views import home, add, create_post_form, post

urlpatterns = [
    path('', home),
    path('add/', add),
    path('create_post/', create_post_form),
    path("<int:id>", post),

]
