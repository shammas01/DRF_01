
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserSerializer,UserRegisterSerializer,UserLoginSerializer,ProfileSerializer,userprofilemodelserializer
from . models import MyUser,UserProfile
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
            user = authenticate(email=email,password=password)
            print(user)
            if user is not None and check_password(password, user.password):
                token = get_tokens_for_user(user)
                response = Response({"token":token,"msg":"user login succeccfully"},status=status.HTTP_200_OK)
                return response
            return Response({"msg":"Incorrect email or passeword"})
        return Response(serializer.errors)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        serializer = userprofilemodelserializer(data=request.data)       
        if serializer.is_valid():
            if not UserProfile.objects.filter(user=request.user).exists():    
                UserProfile.objects.create(
                user=request.user,
                age = serializer.validated_data['age'],
                profile = serializer.validated_data['profile'],
                phone = serializer.validated_data['phone']
            )       
                return Response({"msg":"your profile success fully added"},status=status.HTTP_200_OK)
            return Response({"msg":"your profile is already adedd!"},status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors)

   

    def get(self,request):
        user = UserProfile.objects.filter(user_id=request.user.id).first()
        if user is not None:
            serializer = userprofilemodelserializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        
    def put(self,request):
        user = request.user
        serializer = userprofilemodelserializer(user,data=request.data)
        if serializer.is_valid():
            
            UserProfile.objects.update(
                age = serializer.validated_data['age'],
                profile = serializer.validated_data['profile'],
                phone = serializer.validated_data['phone']
            )
            
            return Response({"msg":"your profile is Updated"},status=status.HTTP_200_OK)
        return Response(serializer.errors)


    def delete(self,request):
        data = UserProfile.objects.get(user = request.user)
        print(data)
        data.delete()
        return Response({"msg":"your profile is deleted"},status=status.HTTP_200_OK)
        


from rest_framework_simplejwt.tokens import RefreshToken
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        print(refresh_token)

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            

            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

       
