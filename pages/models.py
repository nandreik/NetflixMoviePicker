from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# python manage.py makemigrations to make changes to models
# python manage.py migrate to update db with changes


class Movie(models.Model):  # movie model is added to user which is logged in
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    year = models.TextField()
    imdb = models.TextField()
    rg = models.TextField()
    length = models.TextField()
    genre = models.TextField()
    desc = models.TextField()
    image = models.TextField()
    userChoice = models.TextField()

    @classmethod
    def create(cls, request, movieDict):  # idk if this is needed
        return cls(user=request.user,
                   name=movieDict['movieInfo']["name"],
                   year=movieDict['movieInfo']["year"],
                   imdb=movieDict['movieInfo']["imdb"],
                   rg=movieDict['movieInfo']["rg"],
                   length=movieDict['movieInfo']["length"],
                   genre=movieDict['movieInfo']["genre"],
                   desc=movieDict['movieInfo']["desc"],
                   image=movieDict['movieInfo']["image"],
                   userChoice=movieDict["userChoice"])

    def __str__(self):
        return str([self.user.username, self.name, self.year, self.imdb, self.rg, self.length, self.genre, self.desc, self.image, self.userChoice])
