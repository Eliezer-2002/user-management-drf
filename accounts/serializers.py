from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        
        model = User

        fields = ['id', 'username', 'email', 'password', 'confirm_password']

        extra_kwargs = {
            'username': {'validators': []},  # disable automatic unique check
            'email': {'validators': []},
            'password': {'write_only': True}
        }
    
    def validate(self, attrs):
        errors = {}
        
        if attrs['password'] != attrs['confirm_password']:
            errors['password'] = ['Password and Confirm Password do not match']

        if User.objects.filter(username=attrs['username']).exists():
            errors['username'] = ['Username alredy taken']

        if User.objects.filter(is_staff=True,email=attrs['email']).exists():
            errors['email'] = ['Email alredy Registered']
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password'],
            is_staff = True
        )

        return user

    

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        
        model = User

        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password'],
            created_by = self.context['request'].user
        )

        return user

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
