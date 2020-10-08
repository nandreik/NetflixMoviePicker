import json

# library for reading/writing json info until an actual db is implemented


jsonPath = r'data/moviedata.json'
lastUsedPath = r'data/driver_last_used_time'


def update_last_used(newTime):  # update last used time of webdriver
    last_used = {"last_used": newTime}
    with open(lastUsedPath, 'w') as f:
        json.dump(last_used, f, indent=4)


def read_last_used():    # read last used time
    with open(lastUsedPath, 'r') as f:
        data = json.load(f)
    return data


def writeJson(newDict):   # update json file
    with open(jsonPath, 'w') as f:
        json.dump(newDict, f, indent=4)


def readJson():     # fetch json data as dictionary
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


def addMovie(userDict, movieDict):   # append a newly found movie to a user's list
    # get json data
    jsonData = readJson()
    username = userDict["username"]
    movieName = movieDict["movieInfo"]["name"]
    jsonData[username]["movieList"][movieName] = movieDict
    # write to json file
    writeJson(jsonData)


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


def checkMovie(userDict, movieDict):  # check if a movie is not in a user's list
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


def findCommonMovies(user, otherUser):  # return list of common movies between two users
    commonMovies = []   # list of dict movie pairs
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
