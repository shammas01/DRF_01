
from rest_framework.views import APIView
from rest_framework.response import Response
from . serializers import UserSerializer
from . models import User
from rest_framework.permissions import IsAuthenticated,IsAdminUser

# Create your views here.

class UserRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save() 
            response = Response({"data":serializer.data,"msg":"user successfully registerd"})
            return response
        return Response(serializer.errors)


    