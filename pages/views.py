import ast
import threading

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from webdriver import webscraper
from .models import Movie
from .apps import Global_Driver, init_driver, shutdown

# rest stuff
from rest_framework import viewsets, permissions, status, generics, mixins, renderers
from .models import MovieSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


# handle request/response logic
# Create your views here.
from .permissions import IsOwnerOrReadOnly

lock = threading.Lock()  # global lock for find_movie()


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class SignupPageView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class FindMoviePageView(generic.ListView):
    template_name = "findmovie.html"
    model = Movie
    movie_dict = None  # place holder for movie find by webdriver

    def post(self, request):
        global Global_Driver
        print(Global_Driver)
        if Global_Driver is None:
            Global_Driver = init_driver()
            print(Global_Driver)

        if request.POST.get('spin-btn'):  # handle spin button
            self.find_movie(Global_Driver)

        elif request.POST.get('yes-btn'):  # handle yes button
            self.movie_dict = ast.literal_eval(request.POST['yes-btn'])  # get movie info from found movie
            if self.movie_dict:
                self.movie_dict["userChoice"] = "Yes"
                # create movie model from movie_dict and save it to current user
                self.model = Movie.create(request, self.movie_dict)
                self.model.save()

            self.find_movie(Global_Driver)

        elif request.POST.get('no-btn'):  # handle no button
            self.movie_dict = ast.literal_eval(request.POST['no-btn'])  # get movie info from found movie
            if self.movie_dict:
                self.movie_dict["userChoice"] = "No"
                # create movie model from movie_dict and save it to current user
                self.model = Movie.create(request, self.movie_dict)
                self.model.save()

            self.find_movie(Global_Driver)

        return render(request, self.template_name, {'movie': self.movie_dict})

    def find_movie(self, driver):
        global lock
        print("Trying to acquire lock.")
        with lock:
            print("Locked")
            self.movie_dict = webscraper.findMovie(driver)
            if len(self.movie_dict["movieInfo"]["image"]) < 5:  # check to see if there is a real src image to return
                self.movie_dict["movieInfo"]["image"] = None
            self.check_dict(self.movie_dict)
        print("Released")

    def check_dict(self, movie):  # check movie dict for any not found attributes to avoid key error when adding to db
        print(movie)
        if "name" not in movie['movieInfo'].keys():
            movie['movieInfo']['name'] = ""
        if "year" not in movie['movieInfo'].keys():
            movie['movieInfo']['year'] = ""
        if "imdb" not in movie['movieInfo'].keys():
            movie['movieInfo']['imdb'] = ""
        if "rg" not in movie['movieInfo'].keys():
            movie['movieInfo']['rg'] = ""
        if "length" not in movie['movieInfo'].keys():
            movie['movieInfo']['length'] = ""
        if "genre" not in movie['movieInfo'].keys():
            movie['movieInfo']['genre'] = ""
        if "desc" not in movie['movieInfo'].keys():
            movie['movieInfo']['desc'] = ""
        if "image" not in movie['movieInfo'].keys():
            movie['movieInfo']['image'] = ""
        print(movie)


class FindFriendPageView(TemplateView):
    template_name = "findfriend.html"
    friend = None
    notFound = False  # bool to track if a friend is a user in the db
    movies = None  # common movies between user and friend


    def post(self, request):

        if request.POST.get('find-btn'):  # handle find
            # check if friend is user
            if User.objects.filter(username__iexact=request.POST['friend']).exists():
                print("Friend Exists")
                self.friend = User.objects.get(username__iexact=request.POST['friend'])
                # find User's and Friend's movies
                userMovies = Movie.objects.filter(user=request.user)
                friendMovies = Movie.objects.filter(user=self.friend)
                # find common movies
                self.movies = []
                for uMovie in userMovies:
                    for fMovie in friendMovies:
                        if uMovie.name == fMovie.name and uMovie.userChoice == "Yes" and fMovie.userChoice == "Yes":
                            self.movies.append(uMovie)

            else:
                print("Friend DNE")
                self.notFound = True

            return render(request, self.template_name, {'friend': self.friend,
                                                        'notFound': self.notFound,
                                                        'commonMovies': self.movies})


# rest stuff

class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



"""
api requests with class based views  
"""


class MovieDetail(APIView):
    """
    Retrieve, update or delete a movie instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_object(self, name, user_pk):    # get movie with matching name, for the currently logged in user
        try:
            print("TEST", user_pk)
            return Movie.objects.get(name=name, user=user_pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        movie = self.get_object(name, request.user.id)
        serializer = MovieSerializer(movie, context={'request': request})
        return Response(serializer.data)

    def put(self, request, name, format=None):
        movie = self.get_object(name, request.user.id)
        serializer = MovieSerializer(movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        movie = self.get_object(name, request.user.id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieList(APIView):
    """
    List all movies, or create a new movie.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
api requests with methods 
"""
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     """
#     List all movies, or create a new movie.
#     """
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True, context={'request': request})   # need to add context, otherwise get hyperlink error
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = MovieSerializer(data=data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, name):
#     """
#     Retrieve, update or delete a movie.
#     """
#     try:
#         movie = Movie.objects.get(name=name, user=request.user.id)
#     except Movie.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = MovieSerializer(movie, context={'request': request})
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = MovieSerializer(movie, data=data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         movie.delete()
#         return HttpResponse(status=204)




