from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.


class User(AbstractUser):
    ROLL_CHOICES=(
        ('CANDIDATE','Candidate'),
        ('RECURITER','Recuriter'),
        ('Admin','Admin')
    )
    role=models.CharField(max_length=20,choices=ROLL_CHOICES,default='ADMIN')
    email=models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username
    

class Company(models.Model):
    name=models.CharField(max_length=30)
    location=models.CharField(max_length=20)
    industry=models.CharField(max_length=20)
    website=models.URLField(blank=True)
    employee_count=models.PositiveIntegerField()
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    