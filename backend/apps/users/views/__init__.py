from django.urls import path
from rest_framework.routers import DefaultRouter

from .user import LoginView, RegisterView, UserListView

router = DefaultRouter()

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UserListView.as_view(), name="user-list"),
]


__all__ = ["urlpatterns"]
