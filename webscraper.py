from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import unicodedata
import json
from os.path import join


def initDriver():   # connect web driver to roulette url
    url = "https://reelgood.com/roulette/netflix"
    # driverPath = r'C:\Users\Nikita\PycharmProjects\NetflixMoviePicker\webdriver\geckodriver.exe'
    driverPath = r'webdriver/geckodriver.exe'
    options = Options()
    options.headless = True  # run browser windowless
    driver = webdriver.Firefox(options=options, executable_path=driverPath)
    driver.get(url)
    return driver


def initSpin(driver):   # set up spin options for movies only and any score
    # genre is set to all genres by default
    # imdb score is set to any by default
    # uncheck TV Shows in type to only spin for movies
    tvButton = driver.find_element_by_xpath(
        "/html/body/div[1]/div[3]/main/div[2]/div[2]/div[1]/div[1]/div[2]/div/label[2]/span[1]")
    tvButton.click()
    # set rg score to any
    rgMenu = driver.find_element_by_xpath(
        "/html/body/div[1]/div[3]/main/div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[1]")  # click open rg score menu
    rgMenu.click()
    rgAnyScore = driver.find_element_by_xpath(
        "/html/body/div[1]/div[3]/main/div[2]/div[2]/div[1]/div[1]/div[4]/div/div/div[2]/div[6]")  # click on any score option
    rgAnyScore.click()
    return driver


def findMovie(driver):  # spin for a movie and return its info as json string
    # spin
    spinButton = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/div[2]/div[1]/div[2]/button")
    spinButton.click()
    # find movie details
    time.sleep(.25)  # wait a bit to let movie info load, otherwise may try to read before it is loaded
    movie = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/div[2]/div[2]/div").text.splitlines()
    infoTemp = ["name", "year", "imdb", "rg", "length", "genre", "desc"]
    movieDict = {}  # dict for name only that holds dict with movie info
    movieInfo = {}  # dictionary for movie information
    for i in range(len(movie) - 2):
        key = infoTemp[i]
        val = unicodedata.normalize('NFKD', movie[i]).encode('ascii', 'ignore')     # normalize unicode, some movies can have weird chars that don't translate to ascii well
        movieInfo[key] = val
    # add the movie image because why not
    image = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/div[2]/div[2]/a/div/div/picture/img").get_attribute("src")
    movieInfo["image"] = image
    # add key for user decision for movie ("yes"/"no")
    movieDict["userChoice"] = ""
    # add movie info dict to movieDict
    movieDict["movieInfo"] = movieInfo
    print movieDict
    return movieDict


def writeJson(newDict):   # update json file
    jsonPath = r'moviedata/moviedata.json'
    jsonDict = readJson()
    # jsonDict[newDict["username"]] = newDict
    with open(jsonPath, 'w') as f:
        json.dump(newDict, f, indent=4)


def readJson():     # fetch json data as dictionary
    jsonPath = r'moviedata/moviedata.json'
    with open(jsonPath, 'r') as f:
        data = json.load(f)
        # print data
    return data


def createUser():      # create a user json object
    username = raw_input("Username: ")
    password = raw_input("Password: ")
    user = {
        "username": username,
        "password": password,
        "movieList": dict()
    }
    # print user
    return user


def appendMovie(username, password, movieDict):   # append a newly found movie to a user
    # get json data
    jsonData = readJson()
    # check if username exists
    if username in jsonData.keys():
        if password == jsonData[username]["password"]:      # check pass
            if movieDict not in jsonData[username]["movieList"].keys():     # check movie not duplicate
                jsonData[username]["movieList"][movieDict["movieInfo"]["name"]] = movieDict
    # write to json file
    writeJson(jsonData)


if __name__ == "__main__":
    # set up web driver and correct options for spin
    webDriver = initDriver()
    initSpin(webDriver)
    movieDict = findMovie(webDriver)
    # jsonData = readJson()
    # userDict = createUser()
    # writeJson(userDict)
    appendMovie("user", "pass", movieDict)
    # spin until new movie found
        # once new movie found, ask user YES/NO
        # add movie to DB for user with YES/NO answer
    webDriver.close()




