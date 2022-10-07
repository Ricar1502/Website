from django.urls import path
from .views import PostView, UserView, RanksView

urlpatterns = [
    path('post', PostView.as_view()),
    path('user', UserView.as_view()),
    path('ranks', RanksView.as_view())
]
