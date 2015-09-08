from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

# Create your models here.



class UserRegister(models.Model):
    # auth = models.OneToOneField(User)
    name = models.CharField(max_length = 50)
    gender = models.CharField(max_length = 10)
    age = models.CharField(max_length = 4)
    mail_id = models.CharField(max_length = 100)
    phone_no = models.CharField(max_length = 15)
    address = models.CharField(max_length = 200)
    password = models.CharField(max_length = 100)



class DonorsContriDetails(models.Model):
    username = models.CharField(max_length =100)
    project = models.CharField(max_length = 100)
    scheme = models.CharField(max_length = 100)
    hscheme=models.CharField(max_length=100)
    amount = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100)
    paid_date = models.CharField(max_length = 100)



class ProjectsAndSchemes(models.Model):
    project = models.CharField(max_length = 200)
    scheme = models.CharField(max_length = 200)

class DonorProject(models.Model):
    user = models.CharField(max_length = 100)
    project = models.CharField(max_length = 200)
    scheme = models.CharField(max_length=100)
    subscheme=models.TextField(default=[])