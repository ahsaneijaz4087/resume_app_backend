# users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token  # DRF's built-in Token
from .models import CustomUser
from .serializers import CustomUserSerializer  # Assuming you have this

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Register a new user and return an authentication token.
    """
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create or get token using DRF's standard Token model
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User created successfully',
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Optional: Add a simple login view if you don't have one yet
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login and return authentication token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {
                'username': user.username,
                'email': user.email,
                'user_type': user.user_type
            }
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)