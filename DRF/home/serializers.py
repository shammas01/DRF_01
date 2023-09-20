from . models import MyUser,UserProfile,Shammas
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response 
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','email','username','password']



class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = MyUser
        fields = ['email','username','password','password2']

    def validate(self,data):
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        print(password2,password)

        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('email is alredy exist')
        print(email)
        if password != password2:
            raise ValidationError("password dosn't mach")
        print(password,password2)
        return data
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = MyUser
        fields = ['email','password']





class shammasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shammas
        fields ='__all__'  



class ProfileSerializer(serializers.ModelSerializer):
    shammas = shammasSerializer(many=True)
    class Meta:
        model = UserProfile
        fields =['phone','age','shammas'] 



class userprofilemodelserializer(serializers.ModelSerializer):
    userprofile = ProfileSerializer(many=True)
    class Meta:
        model = MyUser   
        fields =['email','username','userprofile']
     
        
