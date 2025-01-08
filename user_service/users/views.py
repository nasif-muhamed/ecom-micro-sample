from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        


class UsersView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            print(users)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Users not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
