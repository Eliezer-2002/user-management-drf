from django.urls import path
from .views import RegisterUserView, UserListView, UserCreateView, UserDetailView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('users/', UserListView.as_view()),
    path('users/create/', UserCreateView.as_view()),
    path('users/<int:pk>/retrieve/', UserDetailView.as_view()),
    path('users/<int:pk>/update/', UserDetailView.as_view()),
    path('users/<int:pk>/delete/', UserDetailView.as_view()),
]