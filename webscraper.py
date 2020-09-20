from os.path import join
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions
from time import sleep
from unicodedata import normalize
import json


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
    # check for popup, if it exists then exit it
    try:
        popupExit = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div[1]/span")
        popupExit.click()
        # print("Popup Exited")
    # except exceptions.NoSuchElementException:
        # print("No Popup Found")
    finally:
        # spin
        spinButton = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/div[2]/div[1]/div[2]/button")
        spinButton.click()
        # find movie details
        sleep(.25)  # wait a bit to let movie info load, otherwise may try to read before it is loaded
        movieElem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/div[2]/div[2]/div").text.splitlines()
        infoTemp = ["name", "year", "imdb", "rg", "length", "genre", "desc"]
        movie = {}  # dict for name only that holds dict with movie info
        movieInfo = {}  # dictionary for movie information
        for i in range(len(movieElem) - 2):
            key = infoTemp[i]
            val = normalize('NFKD', movieElem[i]).encode('ascii', 'ignore')     # normalize unicode, some movies can have weird chars that don't translate to ascii well
            movieInfo[key] = val.decode('utf-8')
        # add the movie image because why not
        image = driver.find_element_by_xpath("/html/body/div[1]/div[3]/main/div[2]/div[2]/div[2]/a/div/div/picture/img").get_attribute("src")
        movieInfo["image"] = image
        # add key for user decision for movie ("yes"/"no")
        movie["userChoice"] = ""
        # add movie info dict to movieDict
        movie["movieInfo"] = movieInfo
        return movie


def writeJson(newDict):   # update json file
    jsonPath = r'moviedata/moviedata.json'
    with open(jsonPath, 'w') as f:
        json.dump(newDict, f, indent=4)


def readJson():     # fetch json data as dictionary
    jsonPath = r'moviedata/moviedata.json'
    with open(jsonPath, 'r') as f:
        data = json.load(f)
    return data


def createUser():      # create a new user json object
    while True:
        username = input("Username: ")
        password = input("Password: ")
        passwordConfirm = input("Confirm Password: ")
        if password != passwordConfirm:
            print("Passwords Do Not Match")
        else:
            break
    user = {
        "username": username,
        "password": password,
        "movieList": {}
    }
    return user


def addUser(userDict):  # add new user to DB
    jsonData = readJson()
    username = userDict["username"]
    if username not in jsonData.keys():
        jsonData[username] = userDict
        writeJson(jsonData)
        print("User Added Successfully")
    else:
        print("User Already Exists")


def loginUser():    # get user login and check it is correct
    username = input("Username: ")
    password = input("Password: ")
    user = {
        "username": username,
        "password": password,
        "movieList": {}
    }
    # check if user in db
    jsonData = readJson()
    if username in jsonData.keys():
        if password in jsonData[username]["password"]:  # check pass
            print("Login Successful")
            return user
        else:
            print("Wrong Password")
    else:
        print("Username Not Found")
    return None


def addMovie(userDict, movieDict):   # append a newly found movie to a user's list
    # get json data
    jsonData = readJson()
    username = userDict["username"]
    movieName = movieDict["movieInfo"]["name"]
    jsonData[username]["movieList"][movieName] = movieDict
    # write to json file
    writeJson(jsonData)


def checkMovie(userDict, movieDict):    # check if a movie is not in a user's list
    # get json data
    jsonData = readJson()
    # check if username exists
    username = userDict["username"]
    password = userDict["password"]
    if username in jsonData.keys():
        if password in jsonData[username]["password"]:  # check pass
            movieName = movieDict["movieInfo"]["name"]
            if movieName not in jsonData[username]["movieList"]:  # check movie not duplicate
                return True
    return False


def loginMenu(driver, userDict):
    while True:
        print("___LOGIN OPTIONS___\n"
              "1: FIND MOVIE\n"
              "2: COMPARE MOVIES\n"
              "3: EXIT")
        print("ENTER 1-3:")
        choice = int(input())
        if choice == 1:
            # enter spin menu
            spinMenu(driver, userDict)
            break
        elif choice == 2:
            # enter name of other user
            print("ENTER OTHER USERNAME: ")
            otherUser = input()
            compareMenu(userDict, otherUser)
        elif choice == 3:
            print("EXITING")
            break
        else:
            print("INPUT 1-3 ONLY")


def compareMenu(userDict, otherUsername):
    while True:
        print("___COMPARE OPTIONS___\n"
              "1: SHOW COMMON MOVIES\n"
              "2: SHOW", userDict["username"], "'s Movies\n"
              "3: SHOW", otherUsername, "'s Movies\n"
              "4: EXIT")
        print("ENTER 1-4:")
        choice = int(input())
        if choice == 1:
            print("Common Movies")
            commonMovies = findCommonMovies(userDict["username"], otherUsername)
            for i in range(len(commonMovies)):
                print((i + 1), "\t", [x for x in commonMovies[i]["movieInfo"].values()])
        elif choice == 2:
            print(userDict["username"].join("'s Movies"))
            jsonData = readJson()
            count = 1
            for m in jsonData[userDict["username"]]["movieList"]:
                print(count, "\t", jsonData[userDict["username"]]["movieList"][m])
                count += 1
        elif choice == 3:
            print(otherUsername.join("'s Movies"))
            jsonData = readJson()
            count = 1
            for m in jsonData[otherUsername]["movieList"]:
                print(count, "\t", jsonData[otherUsername]["movieList"][m])
                count += 1
        elif choice == 4:
            break
        else:
            print("INPUT 1-4 ONLY")


def findCommonMovies(user, otherUser):  # return list of common movies between two users
    commonMovies = []
    jsonData = readJson()
    userMovies = (jsonData[user]["movieList"])
    otherUserMovies = (jsonData[otherUser]["movieList"])
    for movie in userMovies.values():
        movieName = movie["movieInfo"]["name"]
        if movie["userChoice"] == "Yes":
            if movie in otherUserMovies.values():
                if otherUserMovies[movieName]["userChoice"] == "Yes":
                    commonMovies.append(movie)
    return commonMovies


def spinMenu(driver, userDict):
    while True:
        print("___SPIN OPTIONS___\n"
              "1: FIND MOVIE\n"
              "2: EXIT")
        print("ENTER 1-2:")
        choice = int(input())
        if choice == 1:
            movieMenu(driver, userDict)
        elif choice == 2:
            break
        else:
            print("INPUT 1-2 ONLY")


def movieMenu(driver, userDict):
    while True:
        print("___MOVIE INFO___")
        movieDict = findMovie(driver)
        if checkMovie(userDict, movieDict):
            for item in movieDict["movieInfo"].values():
                print(item)
            print("DO YOU WANT TO WATCH THIS MOVIE?\n"
                  "1: YES\n"
                  "2: NO\n"
                  "3: EXIT")
            print("ENTER 1-3:")
            choice = int(input())
            if choice == 1:
                # update movie's user choice
                movieDict["userChoice"] = "Yes"
                # add movie
                addMovie(userDict, movieDict)
            elif choice == 2:
                # update movie's user choice
                movieDict["userChoice"] = "No"
                addMovie(userDict, movieDict)
            elif choice == 3:
                break
            else:
                print("INPUT 1-3 ONLY")


def initMenu():
    while True:
        print("___HOME OPTIONS___\n"
              "1: LOGIN\n"
              "2: CREATE USER\n"
              "3: EXIT")
        print("ENTER 1-3:")
        choice = int(input())
        if choice == 1:
            # login menu
            user = loginUser()
            return user
        elif choice == 2:
            # create user
            user = createUser()
            addUser(user)
            return user
        elif choice == 3:
            break
        else:
            print("INPUT 1-3 ONLY")


if __name__ == "__main__":
    # login/create user
    user = initMenu()
    if user:
        try:
            # set up web driver and correct options for spin
            webDriver = initDriver()
            initSpin(webDriver)
            # launch menu
            loginMenu(webDriver, user)
        finally:
            # close/quit driver
            webDriver.close()
            webDriver.quit()
