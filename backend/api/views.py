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
    queryset=Company.objects.all()
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



class CandiateCreateListApi(generics.ListCreateAPIView):
    queryset=Candidate.objects.all()
    serializer_class=CandiateSerializer
    permission_classes=[IsAuthenticated]


    def get_queryset(self):
        return Candidate.objects.filter(user=self.request.user)
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class jobListCreateApi(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if request.user.role != 'RECURITER':
            return Response(
                {
                    "error": "Only recruiter can create jobs"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        job_count = Job.objects.filter(
            recruiter=request.user
        ).count()

        if job_count >= 10:
            return Response(
                {
                    "error": "Maximum 10 jobs allowed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            recruiter=request.user
        )

        return Response(
            {
                "message": "Job created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(
            recruiter=self.request.user
        )

        
      










   