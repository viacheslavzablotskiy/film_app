from django.urls import path
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'signup', views.RegistrationView, basename='signup'),
router.register(r'activate', views.ActivationView, basename='activate'),
router.register(r'login', views.LogInView, basename='login'),
router.register(r'access_token', views.AccessTokenView, basename='access_token'),


urlpatterns = [
    # path("register/", views.RegistrationView.as_view(), name="create-user"),
    path('google/', views.google_login),
    path('google_logout/', views.google_logout),
    path('me/', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('message/(?P<token>[a-z0-9-]+)/', views.verify, name="message"),
    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),

    path('social/', views.SocialLinkView.as_view({'get': 'list', 'post': 'create'})),
    path('social/<int:pk>/', views.SocialLinkView.as_view({'put': 'update', 'delete': 'destroy'})),
        ]
urlpatterns += list(router.urls)
