# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import app as celery_app
#
# __all__ = ('celery_app',)


"""
directions for deploying to heroku

1: git clone https://github.com/nandreik/NetflixMoviePicker.git
2: cd NetflixMoviePicker
3: heroku create netflixmovieroulette
3.1: add buildpacks for driver in heroku app settings
    # Python: heroku/python
    # Headless Google Chrome: https://github.com/heroku/heroku-buildpack-google-chrome
    # Chromedriver: https://github.com/heroku/heroku-buildpack-chromedriver
    heroku buildpacks:add heroku/python
    heroku buildpacks:add https://github.com/heroku/heroku-buildpack-chromedriver
    heroku buildpacks:add https://github.com/heroku/heroku-buildpack-google-chrome

    heroku buildpacks:add https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku/google-chrome.tgz
    heroku buildpacks:add https://buildpack-registry.s3.amazonaws.com/buildpacks/heroku/chromedriver.tgz
3.2: add config vars through cmd
    heroku config:set GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google_chrome
    heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver

    # heroku config:set GOOGLE_CHROME_SHIM=/app/.apt/opt/google/chrome/google-chrome

4: git push heroku master
5: heroku ps:scale web=1
6: heroku open

heroku logs --tail
"""