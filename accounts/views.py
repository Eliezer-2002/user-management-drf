from django.shortcuts import render, redirect
from rest_framework import generics, permissions, filters
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer
from .pagination import UserPagination
from .permissions import IsMainUser

class RegisterUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(created_by=user)

    serializer_class = UserSerializer
    permission_classes = [IsMainUser]
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

class UserCreateView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]

# class UserUpdateView(generics.UpdateAPIView):

#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsMainUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMainUser]



# Page Renders 

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def users_page(request):
    return render(request, 'users.html')
