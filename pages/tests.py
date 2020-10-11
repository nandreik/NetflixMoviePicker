from django.test import TestCase, SimpleTestCase
from .models import Movie, User
from django.contrib.auth import get_user_model
from webdriver import webscraper
from django.urls import reverse


# TestCase for db, SimpleTestCase for without db


class SimpleTests(SimpleTestCase):
    # tested in homepagetests
    # def test_home_page_status_code(self):
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)

    def test_about_page_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_findfriend_page_status_code(self):
        response = self.client.get('/findfriend/')
        self.assertEqual(response.status_code, 200)

    def test_findmovie_page_status_code(self):
        response = self.client.get('/findmovie/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    # tested in signuppagetests
    # def test_signup_page_status_code(self):
    #     response = self.client.get('/accounts/signup/')
    #     self.assertEqual(response.status_code, 200)

    # def test_password_change_done_page_status_code(self):   #
    #     response = self.client.get('/accounts/password_change/done/')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_password_change_from_page_status_code(self):   #
    #     response = self.client.get('/accounts/password_change/')
    #     self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_page_status_code(self):
        response = self.client.get('/accounts/reset/done/')
        self.assertEqual(response.status_code, 200)

    # def test_password_reset_confirm_page_status_code(self):     #
    #     response = self.client.get('/accounts/reset/MQ/set-password/')
    #     self.assertEqual(response.status_code, 200)

    def test_password_reset_done_page_status_code(self):
        response = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_form_page_status_code(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)


class HomePageTests(SimpleTests):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'

    def test_signup_page_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):  #
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class MovieModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="user",
                                                         email="test@email.com",
                                                         password="password")

        self.movie = Movie.objects.create(user=self.user,
                                          name="movie name",
                                          year="year",
                                          imdb="imdb",
                                          rg="rg",
                                          length="length",
                                          genre="genre",
                                          desc="desc",
                                          image="image",
                                          userChoice="choice")

    # def tearDown(self):
    #     self.driver.quit()

    def test_string_representation(self):
        movie = Movie.objects.get(id=1)
        expected = str(['user', 'movie name', 'year', 'imdb', 'rg', 'length', 'genre', 'desc', 'image', 'choice'])
        self.assertEqual(str(movie), expected)

    def test_user_content(self):
        testuser = self.user
        expected = [testuser.username, testuser.email]
        self.assertEqual(['user', 'test@email.com'], expected)

    def test_movie_content(self):
        self.assertEqual(f'{self.movie.user}', 'user')
        self.assertEqual(f'{self.movie.name}', 'movie name')
        self.assertEqual(f'{self.movie.year}', 'year')
        self.assertEqual(f'{self.movie.imdb}', 'imdb')
        self.assertEqual(f'{self.movie.rg}', 'rg')
        self.assertEqual(f'{self.movie.length}', 'length')
        self.assertEqual(f'{self.movie.genre}', 'genre')
        self.assertEqual(f'{self.movie.desc}', 'desc')
        self.assertEqual(f'{self.movie.image}', 'image')
        self.assertEqual(f'{self.movie.userChoice}', 'choice')

    # test find movie page, find friend page


class FindMovieTest(TestCase):
    def setUp(self):
        self.driver = webscraper.initDriver()

    def tearDown(self):
        self.driver.quit()

    def test_find_movie(self):
        movie = webscraper.findMovie(self.driver)
        check = False
        if movie:
            check = True
        self.assertTrue(check, True)


class FindFriendTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username="user1",
                                                          email="test@email.com",
                                                          password="password")
        self.user2 = get_user_model().objects.create_user(username="user2",
                                                          email="test@email.com",
                                                          password="password")

        self.movie1 = Movie.objects.create(user=self.user1,
                                           name="movie name",
                                           year="year",
                                           imdb="imdb",
                                           rg="rg",
                                           length="length",
                                           genre="genre",
                                           desc="desc",
                                           image="image",
                                           userChoice="Yes")

        self.movie2 = Movie.objects.create(user=self.user2,
                                           name="movie name",
                                           year="year",
                                           imdb="imdb",
                                           rg="rg",
                                           length="length",
                                           genre="genre",
                                           desc="desc",
                                           image="image",
                                           userChoice="Yes")

    def test_same_movie(self):
        user1 = Movie.objects.filter(user=self.user1)
        print("user1: ", user1)
        user2 = Movie.objects.filter(user=self.user2)
        movies = []
        for uMovie in user1:
            for fMovie in user2:
                if uMovie.name == fMovie.name and uMovie.userChoice == "Yes" and fMovie.userChoice == "Yes":
                    movies.append(uMovie)
        self.assertEqual(user1[0].name, movies[0].name)
