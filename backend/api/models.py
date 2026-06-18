from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLL_CHOICES=(
        ('CANDIDATE','Candidate'),
        ('RECURITER','Recuriter'),
        ('Admin','Admin')
    )
    role=models.CharField(max_length=20,choices=ROLL_CHOICES,default='ADMIN')

    def __str__(self):
        return self.username
    