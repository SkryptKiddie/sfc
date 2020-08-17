import os,sys,json,shutil
from tinydb import TinyDB, Query

log = TinyDB("./log.db", indent=4) # upload logging database
logstat = os.stat("./log.db")

with open('./config.json', 'r') as config_file:
    data = json.load(config_file)

WEB_FOLDER = data["WWW_FOLDER"]
CONTAINER_FOLDER = data["WWW_FOLDER"] + "/" + data["CONTAINER_FOLDER"]

def containerStats(): # prints the stats for the container
    print("Current container: " + str(os.getcwd()))
    print("Container size: " + str(sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))) + " bytes")
    print("Container file count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)])))
    print("Upload DB name: " + str(log.name))
    print("Upload DB log count: " + str(len(log)))
    print("Upload DB size: " + str(logstat.st_size) + " bytes.")

#os.chdir(CONTAINER_FOLDER) # change active folder to container
os.chdir(CONTAINER_FOLDER)
print("Simple File Container cleaner \n")
containerStats()

askDel = input("\nDelete all files in the container and clear the upload database? (y/n): ")
if askDel[:1] == "y":
    try:
        #shutil.rmtree(CONTAINER_FOLDER)
        shutil.rmtree(".", ignore_errors=True) # clear the container folder
        log.truncate() # clear the upload database
        print("\nCleared the container successfully!")
        containerStats()

    except:
        print("An error occured while trying to clean the container.")

if askDel[:1] == "n":
    print("Exiting...")
    exit()