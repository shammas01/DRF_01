from . models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.hashers import make_password



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','password']




class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    class Meta:
        model = User
        fields = ['email','password','username','password2']

    def validate(self,validate_data):
        email = validate_data.get('email')
        password = validate_data.get('password')
        password2 = validate_data.get('password2')

        if User.objects.filter(email=email).exists():
            raise ValidationError('email is alredy exist')
        
        if password != password2:
            raise ValidationError("password dosn't mach")

        return validate_data
    

    # def create(self, validated_data):
    #     # Hash the password before saving it to the database
    #     password = validated_data.get('password')
    #     user = User.objects.create_user(**validated_data, password=password)  
    #     return user

    # def create(self, data):
    #     password = data.get('password')
    #     user = User.objects.create_user(**data, password=password)
    #     return user

