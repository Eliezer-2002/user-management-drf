from django.urls import path

from .views import (
    RegisterUserView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserRetrieveView,
    UserUpdateView,
)

urlpatterns = [
    path("newuserregister/", RegisterUserView.as_view(), name="register_user"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    path(
        "users/<int:pk>/retrieve/",
        UserRetrieveView.as_view(),
        name="user_retrieve",
    ),
    path(
        "users/<int:pk>/update/",
        UserUpdateView.as_view(),
        name="user_update",
    ),
    path(
        "users/<int:pk>/delete/",
        UserDeleteView.as_view(),
        name="user_delete",
    ),
]
