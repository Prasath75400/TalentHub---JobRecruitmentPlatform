from  rest_framework import serializers
from .models import *
import re
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,validators=[validate_password])
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('username','email','password','confirm_password','role')


    def validate_password(self,value):
        if len(value)< 6 :
            raise serializers.ValidationError("Password must be at least 8 characters long." ) 

        if not re.search(r'[A-Z]',value):
             raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r'[a-z]',value):
             raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r'[@$!%*?&#]', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('{"confirm_password": "Passwords do not match."}')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create(
          username=validated_data['username'],
          email=validated_data['email'],
         
          role=validated_data['role']
           )
        user.set_password(validated_data['password']) 
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):   
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')

        user=authenticate(
            email=email,
            password=password
        )
        if not user:
             raise serializers.ValidationError( "Invalid username or password" )
        

        refresh=RefreshToken.for_user(user)

        return {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
    
class CompanySerializer(serializers.ModelSerializer):
     class Meta:
         model=Company
         fields='__all__' 

     def validate_website(self,value): 
          if not value.startswith(("http://", "https://")):
            raise serializers.ValidationError(
                "Website must start with http:// or https://"
            )

          return value   
     
     def validate_employee_count(self,value):
         if value < 0:
             raise serializers.ValidationError("Employee count cannot be negative")
         return value
     
    
     
     def update(self, instance, validated_data):
         instance.name=validated_data.get('name',instance.name)
         instance.location=validated_data.get('location',instance.location)
         instance.industry=validated_data.get('industry',instance.industry)
         instance.website=validated_data.get('website',instance.website)
         instance.employee_count=validated_data.get('employee_count',instance.employee_count)
         
         instance.save()
         return instance