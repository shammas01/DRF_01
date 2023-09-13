from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    email = models.CharField(unique=True,max_length=50)
    def __str__(self):
        return self.email
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']






class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE,null=True)
    profile = models.ImageField(upload_to='profile/',null=True,blank=True)
    age = models.IntegerField()
    phone = models.CharField(max_length=10)

    

    


    def user(self):
        return self.user_id.email