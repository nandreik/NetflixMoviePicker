# from __future__ import absolute_import, unicode_literals
#
# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
# from .celery import app as celery_app
#
# __all__ = ('celery_app',)


"""
directions for deploying to heroku

1: git clone proj in cmd
2: cd to cloned proj in cmd
3: heroku create netflixmoviepicker
4: git push heroku master
5: heroku ps:scale web=1
6: heroku open

heroku logs --tail
"""