import os,sys,json,shutil
with open('./config.json', 'r') as config_file:
    data = json.load(config_file)

WEB_FOLDER = data["WWW_FOLDER"]
CONTAINER_FOLDER = data["WWW_FOLDER"] + "/" + data["CONTAINER_FOLDER"]

def containerStats(): # prints the stats for the container
    print("Current container: " + str(os.getcwd()))
    print("Container size: " + str(sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))) + " bytes")
    print("Container file count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)])))
    print("Container contents: " + str(os.listdir(".")))

os.chdir(CONTAINER_FOLDER) # change active folder to container
print("Simple File Container cleaner")
containerStats()

askDel = input("Delete all files in the container? (y/n): ")
if askDel[:1] == "y":
    try:
        #shutil.rmtree(CONTAINER_FOLDER)
        shutil.rmtree(".", ignore_errors=True)
        print("\nCleared the container successfully!")
        containerStats()

    except:
        print("An error occured while trying to clean the container.")

if askDel[:1] == "n":
    print("Exiting...")
    exit()