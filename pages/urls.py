from django.urls import path, include
from . import views

# rest stuff
from django.urls import include, path
from rest_framework import routers


# file to configure urls **must also be included in webapp\urls.py**

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('accounts/signup/', views.SignupPageView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('findmovie/', views.FindMoviePageView.as_view(), name='findmovie'),
    path('findfriend/', views.FindFriendPageView.as_view(), name='findfriend'),

    # router api paths
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/movies/', views.MovieList.as_view(), name='movie-list'),
    path('api/movies/<str:name>/', views.MovieDetail.as_view(), name='movie-detail'),
]

