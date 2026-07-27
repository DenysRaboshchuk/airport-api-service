from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {"password": {"write_only": True, "min_length": 3}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
