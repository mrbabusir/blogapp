from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.serializers import ValidationError
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from .serializers import * 
from django.contrib.auth import get_user_model

#create user views here

class UserCreateView(CreateAPIView):  #new user registrationko starting view.
    queryset = User.objects.all() #all user ko all objects lai queryset ma rakheko
    serializer_class = UserRegistrationSerializer  ##serializing User registratio
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data) ##fetchin serialized data with get_serialize
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user) ## registration process thik cha bhane token create garney
        return Response({"id": user.id, "username": user.username, "token": token.key}, status=status.HTTP_201_CREATED)
class RegisteredUserview(APIView): #alreayd register usersko list
    def get(self, request):
        users = User.objects.all()
        serializers = UserProfileSerializer(users,many = True) 
        return Response (serializers.data, status=status.HTTP_200_OK)
class RegisteredUserDetails(APIView): #user ko detail .,
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializers = UserProfileSerializer(user) 
            return Response (serializers.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error':'user not found'},status=status.HTTP_404_NOT_FOUND
            )
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Validate that both fields are provided
        if email==None and password==None:
            return Response(
                {'error': 'Both email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, email=email , password=password)#authenticating the user via email and password
        if user:
            # login(request,user)
            token, created = Token.objects.get_or_create(user= user)  # Get or create token for the user
            
            # Return the token and any other relevant user data
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials or User is not register'},
                status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to log out
    def post(self, request):
        try:
            token = getattr(request.user, 'auth_token', None)  # Get the user's token getattr checks if the user has an auth_token attribute
            # If the user does not have a token, it means they are not logged in
            if token is None:
                return Response({"error": "No active session found."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                token.delete()  # Delete the token if it exists
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
