from django.shortcuts import render
from rest_framework import filters, generics, permissions

from .models import User
from .pagination import UserPagination
from .permissions import IsMainUser
from .serializers import UserRegisterSerializer, UserSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class OwnedUserQuerysetMixin:
    def get_queryset(self):
        return User.objects.filter(created_by=self.request.user).order_by("id")


class UserListView(OwnedUserQuerysetMixin, generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "email"]


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]


class UserRetrieveView(OwnedUserQuerysetMixin, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]


class UserUpdateView(OwnedUserQuerysetMixin, generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]


class UserDeleteView(OwnedUserQuerysetMixin, generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]


# Page renders

def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def users_page(request):
    return render(request, "users.html")
