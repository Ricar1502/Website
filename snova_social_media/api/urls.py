from django.urls import path
from .views import PostView, UserView

urlpatterns = [
    path('post', PostView.as_view()),
    path('user', UserView.as_view())
]
