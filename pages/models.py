from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

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
        return str([self.user.username, self.name, self.year, self.imdb, self.rg, self.length, self.genre, self.desc,
                    self.image, self.userChoice])


# rest stuff
class MovieSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Movie
        fields = ["user", "name", "year", "imdb", "rg", "length", "genre", "desc", "image", "userChoice", 'highlight']

    def create(self, validated_data):
        """
        Create and return a new `Movie` instance, given the validated data.
        """
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Movie` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.imdb = validated_data.get('imdb', instance.imdb)
        instance.rg = validated_data.get('rg', instance.rg)
        instance.length = validated_data.get('length', instance.length)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.image = validated_data.get('image', instance.image)
        instance.userChoice = validated_data.get('userChoice', instance.userChoice)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'username', 'email']
