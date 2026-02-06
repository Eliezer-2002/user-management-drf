from django.shortcuts import render
from rest_framework import generics, permissions, filters
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .pagination import UserPagination
from .permissions import IsSuperUser

class RegisterUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):

    queryset = User.objects.filter(is_superuser=False).order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class UserCreateView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

class UserUpdateView(generics.UpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]



# Page Renders 

def login_page(request):
    return render(request, 'login.html')

def users_page(request):
    return render(request, 'users.html')
