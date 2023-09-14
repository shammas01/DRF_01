from . models import MyUser,UserProfile
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password



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






class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email','username']  


class userprofilemodelserializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    class Meta:
        model = UserProfile
        fields = '__all__'