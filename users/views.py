from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from rest_framework import viewsets, permissions
from users.permissions import IsAdmin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {"detail": "User created successfully"},
            status=status.HTTP_201_CREATED
        )


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # JWT login only

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data   # user returned from serializer

        #  Django SESSION LOGIN (needed for request.user)
        # login(request, user)

        #  JWT TOKENS
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role
            },
            "redirect_url": self.get_redirect_url(user.role)
        }, status=status.HTTP_200_OK)

    def get_redirect_url(self, role):
        if role == "admin":
            return "/dashboard/admin/"
        elif role == "mechanic":
            return "/dashboard/mechanic/"
        return "/dashboard/customer/"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['username'] = self.user.username
        data['role'] = self.user.role if hasattr(self.user, 'role') else 'customer'
        return data

@method_decorator(csrf_exempt, name='dispatch')
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def home_page(request):
    return render(request, "auth/home.html")

def register_page(request):
    return render(request, 'auth/register.html')

def login_page(request):
    return render(request, 'auth/login.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    # FILTER USERS BY ROLE (needed for assigning mechanic)
    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get("role")

        if role:
            queryset = queryset.filter(role=role)

        return queryset
       

