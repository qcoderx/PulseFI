from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SmeRegisterSerializer, LenderRegisterSerializer, UserLoginSerializer, UserSerializer
from .models import User

class SmeRegisterView(generics.CreateAPIView):
    """
    Handles POST /auth/sme/register
    """
    queryset = User.objects.all()
    serializer_class = SmeRegisterSerializer

class LenderRegisterView(generics.CreateAPIView):
    """
    Handles POST /auth/lender/register
    """
    queryset = User.objects.all()
    serializer_class = LenderRegisterSerializer

class LoginView(APIView):
    """
    Handles POST /auth/login
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user_type = serializer.validated_data['user_type']

        user = authenticate(request, email=email, password=password)

        if user is not None and user.user_type == user_type:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            
            return Response({
                'token': str(refresh.access_token),
                'user': user_data,
                'user_type': user.user_type
            }, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid credentials or user type.'}, status=status.HTTP_401_UNAUTHORIZED)