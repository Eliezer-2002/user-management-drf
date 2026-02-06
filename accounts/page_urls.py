from django.urls import path
from .views import login_page, users_page

urlpatterns = [
    path('', login_page, name='login'),
    path('users/', users_page),
]