from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('add/', add),
    path('create_post/', create_post_form),
    path("<int:id>", viewPost),
    path("user/<int:id>", view_user),
    path("user/<int:id>/profile", view_updateProfile),
    path("user/<int:id>/delete", view_deleteProfile),
    path("search/",  search_view),
    path('logout/', logout_page),
    path("login/",  login_page),
    path("register/",  register_page),
    path("vote/", vote_view),
    path("new/", new_page),
    path("best/", best_page),
    path("controversial/", controversial_page),
    # path("chat/", chat_page),
    path("chat/<int:id>", chat_page),
    path("chat/", direct_to_first_chat),
    # path("send/", send_message),

    path("notification/", notification_view)
]
