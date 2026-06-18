from  rest_framework import serializers
from .models import *
import re
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('email','password','confirm_password','role')


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
          email=validated_data['email'],
          password=validated_data['password'],
          role=validated_data['role']
           )
        return user
