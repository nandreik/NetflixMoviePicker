from selenium import webdriver
from selenium.common import exceptions
from time import sleep
from unicodedata import normalize
from data_access_lib import data_access
import os

url = "https://reelgood.com/roulette/netflix"
driverPathChrome = r'webdriver/chromedriver.exe'


def initDriver():   # connect web driver to roulette url
    optionsChrome = webdriver.ChromeOptions()
    # for local deployment
    # optionsChrome.add_argument("--headless")
    # optionsChrome.add_argument("--no-sandbox")
    # optionsChrome.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(executable_path=driverPathChrome, chrome_options=optionsChrome)

    # for heroku deployment
    CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')
    GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN')

    optionsChrome.binary_location = GOOGLE_CHROME_BIN
    optionsChrome.add_argument("--headless")
    optionsChrome.add_argument("--no-sandbox")
    optionsChrome.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=optionsChrome)

    driver.get(url)
    driver = initSpin(driver)
    return driver


def initSpin(driver):   # set up spin options for movies only and any score
    # genre is set to all genres by default
    # imdb score is set to any by default
    # uncheck TV Shows in type to only spin for movies
    tvButton = driver.find_element_by_css_selector("label.css-18syq1s:nth-child(2) > span:nth-child(3)")
    tvButton.click()
    # set rg score to any
    rgMenu = driver.find_element_by_css_selector("div.css-1dsqg0t:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)")
    rgMenu.click()
    rgAnyScore = driver.find_element_by_css_selector(".css-1jcj7xc > div:nth-child(6)")
    rgAnyScore.click()
    print("Website Menu Set Up")
    return driver


def findMovie(driver):  # spin for a movie and return its info as json string
    # check for popup, if it exists then exit it
    try:
        popupExit = driver.find_element_by_css_selector(".css-1y9bki9")
        popupExit.click()

    finally:
        # spin
        spinButton = driver.find_element_by_css_selector(".css-1lm9uo8")
        spinButton.click()
        # find movie details
        sleep(.5)  # wait a bit to let movie info load, otherwise may try to read before it is loaded
        movieElem = driver.find_element_by_css_selector(".css-hin13p").text.splitlines()
        infoTemp = ["name", "year", "imdb", "rg", "length", "genre", "desc"]
        movie = {}  # dict for name only that holds dict with movie info
        movieInfo = {}  # dictionary for movie information
        for i in range(len(movieElem) - 2):
            key = infoTemp[i]
            val = normalize('NFKD', movieElem[i]).encode('ascii', 'ignore')     # normalize unicode, some movies can have weird chars that don't translate to ascii well
            movieInfo[key] = val.decode('utf-8')
        # add the movie image because why not
        try:
            image = driver.find_element_by_css_selector(".css-1sz776d").get_attribute("src")
        except exceptions.NoSuchElementException:
            image = ""
        movieInfo["image"] = image
        # add key for user decision for movie ("yes"/"no")
        movie["userChoice"] = ""
        # add movie info dict to movieDict
        movie["movieInfo"] = movieInfo
        return movie


"""
Below Are Menu Functions for Basic Console Functionality 
"""


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
            commonMovies = data_access.findCommonMovies(userDict["username"], otherUsername)
            for i in range(len(commonMovies)):
                print((i + 1), "\t", [x for x in commonMovies[i]["movieInfo"].values()])
        elif choice == 2:
            print(userDict["username"].join("'s Movies"))
            jsonData = data_access.readJson()
            count = 1
            for m in jsonData[userDict["username"]]["movieList"]:
                print(count, "\t", jsonData[userDict["username"]]["movieList"][m])
                count += 1
        elif choice == 3:
            print(otherUsername.join("'s Movies"))
            jsonData = data_access.readJson()
            count = 1
            for m in jsonData[otherUsername]["movieList"]:
                print(count, "\t", jsonData[otherUsername]["movieList"][m])
                count += 1
        elif choice == 4:
            break
        else:
            print("INPUT 1-4 ONLY")


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
        if data_access.checkMovie(userDict, movieDict):
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
                data_access.addMovie(userDict, movieDict)
            elif choice == 2:
                # update movie's user choice
                movieDict["userChoice"] = "No"
                data_access.addMovie(userDict, movieDict)
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
            user = data_access.loginUser()
            return user
        elif choice == 2:
            # create user
            user = data_access.createUser()
            data_access.addUser(user)
            return user
        elif choice == 3:
            break
        else:
            print("INPUT 1-3 ONLY")


if __name__ == "__main__":
    # login/create user
    user = initMenu()
    if user:
        webDriver = None
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
    else:
        print("User Not Found")
