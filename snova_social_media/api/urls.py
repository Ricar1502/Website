from django.urls import path
from .views import PostView, UserView, RanksView, VotesView, NotificationView

urlpatterns = [
    path('post', PostView.as_view()),
    path('user', UserView.as_view()),
    path('ranks', RanksView.as_view()),
    path('votes', VotesView.as_view()),
    path('notification', NotificationView.as_view())
]
