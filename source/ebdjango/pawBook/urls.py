from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("welcome", views.welcome, name="welcome"),
   path("login", views.login_page, name="login"),
   path("logout", views.logout_view, name="logout_view"),
   path("createaccount", views.create, name="create"),
   path("homepage", views.homepage, name="homepage"),
   path("createpost", views.createpost, name="createpost"),
   path("weatherpost", views.weatherpost, name="weatherpost"),
   path("users", views.users, name="users"),
   path("profile", views.profile, name="profile"),
   path("dogPics", views.dogPics, name="dogPics"),
]