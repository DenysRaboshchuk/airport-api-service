from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
