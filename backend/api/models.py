from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.


class User(AbstractUser):
    ROLL_CHOICES=(
        ('CANDIDATE','Candidate'),
        ('RECURITER','Recuriter'),
        ('ADMIN','Admin')
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

class Candidate (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    full_name=models.CharField(max_length=30)
    phone=models.IntegerField()
    experience = models.PositiveIntegerField()
    education=models.TextField()  
    current_salary=models.IntegerField()
    expected_salary=models.IntegerField()
    resume=models.FileField(upload_to='resumes/')

class Job(models.Model):
    recruiter=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    company=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='company_details')    
    title=models.TextField(max_length=50)
    description=models.TextField(max_length=100)

    salary=models.DecimalField(max_digits=10,decimal_places=2)
    location=models.CharField(max_length=30)
    experience_required=models.PositiveIntegerField()
    vacancies=models.PositiveIntegerField()
 
    

class Application(models.Model):
    STATUS=(
        ('APPLIED','Applied'),
        ('SHORTLISTED','Shortlisted'),
        ('INTERVIEW','Interview'),
        ('SELECTED','Selected'),
        ('REJECTED','Rejected')
    )
    candiate=models.ForeignKey(Candidate,on_delete=models.CASCADE)
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    status=models.CharField(choices=STATUS,default='APPLIED')


    

    