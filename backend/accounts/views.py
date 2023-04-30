from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework import mixins, viewsets, status, parsers
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (RegistrationSerializer, ActivationSerializer, LogInSerializer, AccessTokenSerializer,
                          SocialLinkSerializer, AuthorSerializer, UserSerializer)
from accounts.autorization.generate_token import decode_token
from accounts.models import User, AuthUser, SocialLink
from rest_framework.response import Response
from .my_permission.permission import IsAuthor
from accounts.my_permission.permission import IsAutoregistrationOrReadOnly


def google_logout(request):
    """ Страница входа через Google
    """
    return render(request, 'google_logout.html')


def google_login(request):
    """ Страница входа через Google
    """
    return render(request, 'google.html')


def verify(request, token):
    try:
        user = User.objects.get(verification_uuid=token)
        user.is_verified = True
        user.save()
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")
    return HttpResponse(f"Tank you {user.email}")


class RegistrationView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = {
            "message": "We've send confirmation link on your email."
                       " In oder to activate accounts click the link in the message."
        }

        return Response(data, status=status.HTTP_201_CREATED, )


# Not Ok
class ActivationView(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'token'
    lookup_value_regex = '[\w\.-]+'

    permission_classes = (AllowAny,)
    serializer_class = ActivationSerializer

    def retrieve(self, request, token):

        try:
            data = decode_token(token)
            pk = data.get('pk')
            user = User.objects.get(pk=pk)
        except:
            return Response({
                "token": "Invalid token",
                "description": "Just ensure link is correct or not expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ActivationSerializer(user, data={'is_verified': True}, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'detail': "Your accounts was successfully activated!"
        })


# OK
class LogInView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = LogInSerializer

    def create(self, request):
        serializer = LogInSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data
        )


#
class AccessTokenView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = AccessTokenSerializer

    def create(self, request):
        serializer = AccessTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data
        )


class UserView(viewsets.ModelViewSet):
    """ Просмотр и редактирование данных пользователя
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAutoregistrationOrReadOnly
                          ]

    def get_queryset(self):
        user = self.request.user.id
        my_models = AuthUser.objects.filter(user_id=user)

        if my_models.exists():
            my_models = my_models[0]
            return my_models

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """ Список авторов
    """
    queryset = AuthUser.objects.all().prefetch_related('social_links')
    serializer_class = AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """ CRUD ссылок соц. сетей пользователя
    """
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return SocialLink.objects.all()

    def perform_create(self, serializer):
        user = self.request.user.id
        models_profile = AuthUser.objects.filter(user_id=user).first()
        serializer.save(user_id=models_profile.id)
