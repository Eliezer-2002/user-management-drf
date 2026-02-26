from django.urls import path
from .views import login_page, users_page, register_page

urlpatterns = [
    path('', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('users/', users_page, name='users'),
]