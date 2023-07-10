from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer, UserLoginSerializer


@api_view(['POST'])
def register(request):
    if request.user.is_authenticated:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Login(APIView):
#     def post(self, request):
#         if request.user.is_authenticated:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = UserLoginSerializer(data=request.data)
#
#         if not serializer.is_valid():
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         username = serializer.validated_data['username']
#         password = serializer.validated_data['password']
#
#         user = authenticate(username=username, passowrd=password)
#
#         if user is None:
#             return Response(data={"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
#
#         login(request, user)
#         return Response(status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response(UserSerializer(user).data)

        return Response({'error': "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)

        return Response(status=status.HTTP_200_OK)
