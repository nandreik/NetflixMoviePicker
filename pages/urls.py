from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# file to configure urls **must also be included in webapp\urls.py**
# future note: try heroku for website hosting when ready

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('accounts/signup/', views.SignupPageView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('findmovie/', views.FindMoviePageView.as_view(), name='findmovie'),
    path('findfriend/', views.FindFriendPageView.as_view(), name='findfriend'),
]
