from django.urls import path, include
from .views import signup_func, signin_func, Home

urlpatterns = [
    path("signup/", signup_func, name="signup"),
    path("signin", signin_func, name="signin"),
    path("home/", Home.as_view(), name="home"),
    # path("profile")
]
