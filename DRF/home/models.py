from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    profile = models.ImageField(upload_to='profile/',null=True,blank=True)
    age = models.IntegerField()
    phone = models.CharField(max_length=10)

