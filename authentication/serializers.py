from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(max_length=225, required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'email',)


class LoginAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, allow_blank=False)
    username = serializers.EmailField(max_length=225, required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': "Please fill this username field",
                }
            },
            'password': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': "Please fill this password field",
                }
            },
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(required=True, allow_blank=False,
                                             allow_null=False)
    new_password = serializers.CharField(required=True, allow_blank=False,
                                         allow_null=False)

    class Meta:
        fields = ('current_password', 'new_password')


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=False)
    last_name = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class ShowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('username', 'email')
