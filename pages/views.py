import ast
import threading

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from webdriver import webscraper
from .models import Movie
from .apps import Global_Driver, init_driver, shutdown

# handle request/response logic
# Create your views here.


lock = threading.Lock()     # global lock for find_movie()


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
        print("Released")


class FindFriendPageView(TemplateView):
    template_name = "findfriend.html"
    friend = None
    notFound = False  # bool to track if a friend is a user in the db
    movies = None  # common movies between user and friend

    def post(self, request):
        if request.POST.get('find-btn'):  # handle find
            # check if friend is user
            if User.objects.filter(username=request.POST['friend']).exists():
                print("Friend Exists")
                self.friend = User.objects.get(username=request.POST['friend'])
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
