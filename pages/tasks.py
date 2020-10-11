# import time
#
# from webapp.celery import app
# from .apps import Global_Driver, shutdown
# from data_access_lib import data_access
#
# # scheduled task with celery to check driver
# # global vars dont work with celery workers :(
#
#
# @app.task()             # don't think celery will work with selenium webdriver object
# def check_driver():     # run check every x minutes
#     Last_Used = data_access.read_last_used()
#     elapsedTime = time.time() - float(Last_Used['last_used'])
#     shutdownCheck = False
#     if elapsedTime > 300:
#         shutdownCheck = shutdown()
#         # Global_Driver = None
#         return {'shutdown': shutdownCheck,
#                 'status': 'shutdown',
#                 'last_used': Last_Used['last_used'],
#                 'elapsed_time': elapsedTime}
#     else:
#         return {'shutdown': shutdownCheck,
#                 'status': 'running',
#                 'last_used': Last_Used['last_used'],
#                 'elapsed_time': elapsedTime}
#
#
# @app.task()
# def test():
#     print("celery test")
#
#
# """
# make sure to run redis server and cli exes to use celery locally
#
# run this in second pycharm terminal to start a worker, apparently celery doesn't like windows or something
# celery -A webapp worker --pool=solo -l info
#
# run this in 3rd terminal to also use the scheduled tasks after the worker cmd
# ** delete celerybeat.pid to run in new session
# celery -A webapp beat -l info
# """