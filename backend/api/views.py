from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics,status
from rest_framework.response import Response
# Create your views here.
class RegisterApi(generics.CreateAPIView):
    serializer_class=RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"message": "User registered successfully"},status=status.HTTP_201_CREATED)
    

class LoginApi(generics.CreateAPIView):
    serializer_class=LoginSerializer

    def post(self, request, *args, **kwargs):
        serializers=self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        return Response(
            serializers.validated_data,
            status=status.HTTP_200_OK
        )   