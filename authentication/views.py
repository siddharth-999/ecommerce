from django.contrib.auth import logout, authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests

from .models import User, Token
from .permissions import UserPermission, LoginSignupPermission
from .serializers import UserSerializer, RegisterSerializer, \
    ChangePasswordSerializer, UpdateUserSerializer, ShowUserSerializer, \
    LoginAuthSerializer


class UserSignUpAPIView(GenericAPIView):
    """
    post:
    * API for user signup
    ```
    ```
    """
    permission_classes = (AllowAny, LoginSignupPermission)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email'].lower().strip()
            if User.objects.filter(email__iexact=email).exists():
                return Response({"detail": "This email is already registered"},
                                status=status.HTTP_201_CREATED)
            user = User.objects.create_user(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                password=serializer.validated_data['password'],
                email=email)
            return Response({"token": str(user.user_auth_token.key)},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages,
                            status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginAuthentication(ObtainAuthToken, GenericAPIView):
    permission_classes = (AllowAny, LoginSignupPermission)
    serializer_class = LoginAuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_check = User.objects.get(
                    email__iexact=serializer.validated_data['username'].lower().strip(),
                    is_delete=False, is_active=True)
            except User.DoesNotExist:
                response = \
                    {
                        "detail": "We can't find that email address, please try again!",
                    }
                return Response(response, status.HTTP_404_NOT_FOUND)
            password = serializer.validated_data['password']
            user = authenticate(username=user_check.email, password=password)
            if user and user.is_authenticated:
                login(request, user)
                token_obj = Token.objects.create(user=user)
                return Response({"token": str(token_obj.key)},
                                status=status.HTTP_200_OK)
            return Response({"detail": "The password you entered does not "
                                       "match our records, please try again"},
                            status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutAuthentication(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"detail": "Logged Out Successfully!"},
                            status.HTTP_200_OK)
        except Exception as e:
            print("exception :", str(e))
            return Response({"detail": "Some Error Occurred While Logging Out"},
                            status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, UserPermission,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ShowUserSerializer

    def get_queryset(self):
        email = self.request.user.email
        if email:
            return User.objects.filter(email=email.lower().strip(), is_delete=False)
        return User.objects.none()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdateUserSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return self.serializer_class

    def partial_update(self, request, *args, **kwargs):
        if not str(kwargs.get('pk')).isdigit():
            return Response({"detail": "Invalid request"},
                            status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.get_queryset(), pk=int(kwargs.get('pk')))
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        if request.data and serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            response = serializer.data
            response['detail'] = "User Updated Successfully!"
            return Response(response, status=status.HTTP_200_OK)
        return Response({"detail": serializer.error_messages},
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_queryset()
        user.is_delete = True
        user.is_active = False
        user.save()
        Token.objects.filter(user=user).dalete()
        return Response({"detail": "User deleted Successfully!"},
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post', ])
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True) and request.data:
            if not user.check_password(
                    serializer.validated_data.get('current_password')):
                return Response(
                    {"detail": 'Your Current password was incorrect, please try again!'},
                    status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()
            return Response({'detail': 'Password changed successfully'},
                            status=status.HTTP_201_CREATED)
        return Response({"detail": serializer.error_messages},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', ])
    def me(self, request):
        user = request.user
        return Response(UserSerializer(user).data)
