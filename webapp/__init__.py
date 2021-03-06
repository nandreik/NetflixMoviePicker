# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import app as celery_app
#
# __all__ = ('celery_app',)


"""
directions for deploying to heroku

git clone https://github.com/nandreik/NetflixMoviePicker.git
cd NetflixMoviePicker
heroku create netflixmovieroulette

    add buildpacks for driver in heroku app settings
heroku buildpacks:add heroku/python
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome

    add config vars through cmd
heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome
heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver

git push heroku master
heroku ps:scale web=1
heroku open

heroku logs --tail
"""