from django.urls import path

from film import views

urlpatterns = [
    # path('album/', views.AlbumView.as_view({'get': 'list', 'post': 'create'})),
    # path('album/<int:pk>/', views.AlbumView.as_view({'put': 'update', 'delete': 'destroy'})),
    path("moment_add/", views.MovieMoment.as_view({'post': 'create'})),
    path("moment/", views.MovieMomentDetail.as_view({'get': 'list'})),
    path("moment/<int:pk>/", views.MovieMomentDetail.as_view({'get': 'retrieve'})),
    path('stream-track/<int:pk>/', views.StreamingFileView.as_view()),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path("movie/", views.MovieViewSet.as_view({'get': 'list'})),
    path("movie/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})),
    path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating/", views.AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actor/', views.ActorsViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', views.ActorsViewSet.as_view({'get': 'retrieve'})),

]