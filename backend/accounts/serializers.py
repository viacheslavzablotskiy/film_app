from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import serializers
from accounts.models import User, SocialLink, AuthUser, Follower
from accounts.autorization.backend import identify
from accounts.autorization.backend import authenticate_by_refresh_token, authenticate_by_password


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        allow_blank=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)

    def create(self, validated_data):
        # send_mail(
        #     'Verify your QuickPublisher account',
        #     'Follow this link to verify your account: '
        #     'http://localhost:8000%s' % reverse('create-user'),
        #     'zlava.mag@gmail.com',
        #     ["zlava.mag@gmail.com"],
        #     fail_silently=False,
        # )
        return User.objects.create_user(**validated_data)


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_verified',)

    def update(self, instance, validated_data):
        instance.is_verified = validated_data.get('is_verified')
        instance.save()

        return instance


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField(
        allow_blank=False,
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        allow_blank=False,
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        """Identification"""
        user = identify(email=email)

        """Authentication"""
        authenticate_by_password(user, password=password)

        return user.get_tokens()


class AccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        max_length=250,
        allow_blank=False
    )

    def validate_refresh_token(self, value):
        """Authentication"""
        user = authenticate_by_refresh_token(value)

        return user.get_tokens()


class UserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AuthUser
        fields = ("user", 'avatar', 'country', 'city', 'bio', 'display_name')


class SocialLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SocialLink
        fields = ('id', 'link')


class AuthorSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = AuthUser
        fields = ('id', 'avatar', 'country', 'city', 'bio', 'display_name', 'social_links')


class GoogleAuth(serializers.Serializer):
    """ Сериализация данных от Google
    """
    email = serializers.EmailField()
    token = serializers.CharField()
