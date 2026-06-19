from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics,status
from rest_framework.response import Response
from .pagination import *
from rest_framework.permissions import IsAuthenticated
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
class CompanyCreateListView(generics.ListCreateAPIView):
    queryset=Company.objects.all().order_by('-created_at')
    serializer_class=CompanySerializer
    pagination_class=CompanyPagination
    permission_classes=[IsAuthenticated]
    def create(self, request, *args, **kwargs):
        if request.user.role!='ADMIN':
             return Response(
                {
                    "error": "Only Admin can create companies"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message":
                "Company created successfully",
                "data":
                serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class CompanyUpdateView(generics.UpdateAPIView):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer

   