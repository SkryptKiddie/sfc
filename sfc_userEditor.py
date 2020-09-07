import json, os, sys
import string, random
from tinydb import TinyDB, Query

with open('./testConfig.json', 'r') as config_file:
    configs = json.load(config_file)
log = TinyDB((configs["settings"]["UPLOAD_DB"]), indent=4) # upload database
users = TinyDB((configs["settings"]["USERS_DB"]), indent=4) # user database
search = Query()

def generateString(length):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))

option = input("""
Simple File Container user manager
1. Create new token
2. Delete existing token
3. View all uploads by from a user
4. Exit
""")
if option[:1] == "1":
    print("User creation")
    newUserName = input("User's nickname: ")
    newUserId = (generateString(4)+"-"+generateString(4))
    newUserToken = (generateString(8))
    users.insert({
        "username": str(newUserName),
        "userid": str(newUserId),
        "token": str(newUserToken)
    })
    print("Successfully added new user!")
    print("Username: " + str(newUserName))
    print("User upload token: " + str(newUserToken))
    print("User ID: " + str(newUserId))
    exit()

if option[:1] == "2":
    userDel = input("Input user ID or token: ")
    try:
        if users.contains(search.token == str(userDel)) == True: # check if the input is a token in the database
            users.remove(search.token == str(userDel)) # delete user
            print("Successfully deleted user!")
        else: # if not, check if it's a user ID
            if users.contains(search.userid == str(userDel)) == True:
                users.remove(search.userid == str(userDel)) # delete user
                print("Successfully deleted user!")
            else: # if not; error out
                print("User not found.")
                exit()
    except: # if something goes wrong, print an error
        print("An error occured.")

if option[:1] == "3":
    userFileSearch = input("Input user ID or token: ")
    try:
        if log.contains(search.token == str(userFileSearch)) == True: # check if the token exists
            print(log.search(search.token == str(userFileSearch))) # if it does, print all their uploads
            exit()
        else: # if not, error
            print("No uploads found by this user or token doesn't exist.")
    except: # if something goes wrong, print an error
        print("An error occured.")

if option[:1] == "4":
    print("Exiting...")
    exit()