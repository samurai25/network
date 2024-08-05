
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),
    path("fetch_data", views.fetch_data, name="fetch_data"),
    path("fetch_likes", views.fetch_likes, name="fetch_likes"),
    path("post_data", views.post_data, name="post_data"), 
    path("profile_data/<str:username>/", views.profile_data, name="profile_data"), 
    path("profile/<str:username>/", views.profile, name="profile"),
    path("following_data", views.following_data, name="following_data"),
    path("fetch_following_data", views.fetch_following_data, name="fetch_following_data"),
    path("error", views.error, name="error"), 
    path("edit", views.edit, name="edit"),
]
