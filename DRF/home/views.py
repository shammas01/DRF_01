
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserSerializer,UserRegisterSerializer,UserLoginSerializer
from . models import MyUser
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from . tokens import get_tokens_for_user
from rest_framework.authentication import authenticate
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
# Create your views here.

class UserRegisterView(APIView):
    
    def get(self,request):
        user = MyUser.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=MyUser.objects.create(
                username=serializer.validated_data['username'],
                email = serializer.validated_data['email'],
            )
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            response = Response({"msg":"user successfully registerd"})
            return response
        return Response(serializer.errors)



class UserLoginView(APIView):
    def get(self,request):
        return Response({"msg":"please login with your email and password"})

    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            print(email,password)
            try:
                user = MyUser.objects.get(email=email)
            except MyUser.DoesNotExist:
                user = None
            print(user)
            if user is not None and check_password(password, user.password):
                token = get_tokens_for_user(user)
                response = Response({"token":token,"msg":"user login succeccfully"},status=status.HTTP_200_OK)
                return response
            return Response({"msg":"Incorrect email or passeword"})
        return Response(serializer.errors)



class UserProfileView(APIView):
    def get(self,request):
        pass

        

       
