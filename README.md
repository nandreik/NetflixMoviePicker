# NetflixMovieRoulette
https://netflixmovieroulette.herokuapp.com/

This is is a webapp written by myself in an attempt to learn more about software development and Django.

The purpose of this webapp is to let users vote on movies they would like to watch on Netflix and then compare common movies with another user to make choosing a movie easier.

This webapp utilizes Django as the web-framework, Selenium for webscraping random movies from https://reelgood.com/movies/roulette/netflix, and Heroku for online deployment.

You may ask, "Why wouldn't I just use the reelgood.com website for this purpose?", and to that I say: The reelgood.com website does not allow for comparison of common movies with another user.

## Features 
#### 1) Random netflix movie search
	A random movie is shown for the user, which the user vote Yes or No if they want to watch it 
#### 2) Find a friend with common movies
	A search for another user can show any common movies they may have to make it easier to pick what to watch together 
## Future Feature Considerations
#### 1) Add options to specify movie search (genre, min-rating, year, etc..)
	Adding more search options should not be too hard with selenium
#### 2) Add option to look at a friend's movie list
	A new page to view a friend's movies should be pretty easy to add 
#### 3) Add a working email service for forgotten passwords
 	Currently the forgot password email service is not functional, further research is needed to find the best way to implement this
**If forking this project, please create a 'security.py' file in /webapp following the security_template.py file. This is to protect your SECRET_KEY**
