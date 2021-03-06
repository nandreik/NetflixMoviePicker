from django.apps import AppConfig
from webdriver import webscraper
import os
import atexit

# config file for app


Global_Driver = None    # single global var for the webdriver to initialized on startup


def shutdown():  # close driver on server shutdown
    global Global_Driver
    if Global_Driver:
        Global_Driver.quit()
        print("Global Driver Shutdown", Global_Driver)
        Global_Driver = None


def init_driver():
    driver = webscraper.initDriver()
    print("Global Driver Initialized", driver)
    return driver


class PagesConfig(AppConfig):
    name = 'pages'

    # for local development only
    # def ready(self):
    #     atexit.register(shutdown)
    #     global Global_Driver
    #     if os.environ.get('RUN_MAIN', None) == 'true':  # to not run init twice on "python manage.py runserver"
    #         if Global_Driver is None:
    #             Global_Driver = init_driver()
