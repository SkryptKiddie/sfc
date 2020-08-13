import http, os, sys, json, ssl # simple file storage backend
import random, string, os.path, time # tested on python 3.8.5
from io import BytesIO
from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, CGIHTTPRequestHandler, BaseHTTPRequestHandler
from datetime import datetime
from tinydb import TinyDB, Query

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

log = TinyDB("log.db") # upload logging database
with open('./config.json', 'r') as config_file:
    data = json.load(config_file)

class v: # holds all of the variables from config.json
    SERVER = data["SERVER"]
    API_PORT = data["API_PORT"]
    WEB_PORT = data["WWW_PORT"]
    SSL_STATUS = data["SSL_ENABLED"]
    SSL_KEY = data["SSL_KEY"]
    SSL_CERT = data["SSL_CERT"]
    WEB_FOLDER = data["WWW_FOLDER"]
    CONTAINER_FOLDER = data["WWW_FOLDER"] + "/" + data["CONTAINER_FOLDER"]
    MAX_UPLOAD = data["MAX_UPLOAD_SIZE"]
    FILENAME_LENGTH = data["FILENAME_LENGTH"]
    UPLOAD_TOKEN = data["UPLOAD_TOKEN"]
    UPLOAD_DB = data["UPLOAD_DB"]
    apiURL = ("http://" + str(SERVER) + ":" + str(API_PORT))
    webURL = ("http://" + str(SERVER) + ":" + str(WEB_PORT))

def generateFn(length): # sourced from https://pynative.com/python-generate-random-string/
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return str(result_str) # return the filename

class ReqHandler(BaseHTTPRequestHandler): # handle accidental GET requests to the backend
    def do_GET(self):
        self.send_error(405, message="This API only accepts POST requests")
        self.end_headers()

    def do_POST(self): # handle incoming POST requests
        content_length = int(self.headers["Content-Length"])
        uploader_token = str(self.headers["Token"])
        body = self.rfile.read(content_length)
        response = BytesIO()
        if str(uploader_token) == v.UPLOAD_TOKEN: # checks upload token
            if content_length < v.MAX_UPLOAD: # checks file size
                try: # try to upload the file
                    self.send_response(200, message="Upload recieved")
                    self.send_header("Last-Modified", self.date_time_string(time.time()))
                    self.send_header("Content-type", "text/plain")
                    newFileName=(str(generateFn(v.FILENAME_LENGTH)) + ".txt")
                    with open(str(newFileName), 'w') as newUpload: # sourced from https://www.geeksforgeeks.org/create-an-empty-file-using-python/
                        newUpload.write(str(body)) # store the string that we recieved
                        pass
                    stats = os.stat(newFileName) # print stats for the newly uploaded file in the terminal

                    print("New upload, " + str(newFileName) + " and is " + str(stats.st_size) + " bytes. File count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)])))
                    print(str(v.webURL) + "/c/" + newFileName) # prints the URL to the file
                    log.insert(
                        {"upload_time": self.log_date_time_string(), 
                        "token": v.UPLOAD_TOKEN, 
                        "uploader_ip": str(self.address_string()),
                        "filename": newFileName})

                    link = str.encode(str(v.webURL) + "/c/" + str(newFileName) + "\n")
                    response.write(link) # send the URL to the file
                    self.wfile.write(response.getvalue())
                    self.end_headers()

                except: # in case something happens, tell the client and log it
                    print("An error occured while trying to upload.")
                    self.send_error(500, message="An error occured while trying to upload your file, please try again later")
                    self.end_headers()

            else: # error if file too big
                print("Rejected large upload.")
                self.send_error(431, message="File size exceeds limit") # 431 Request Header Fields Too Large
                self.end_headers()

        else: # error if incorrect token
            print("Rejected unauthorised uploader.")
            self.send_error(401, message="Incorrect or missing upload token") # 401 Unauthorised
            self.end_headers()

# runtime
def prestart():
    os.chdir(v.CONTAINER_FOLDER) # set current directory as set in the WWW variable
    print("Simple File Container API")
    print("URL: " + str(v.apiURL))
    print("Current container: " + str(os.getcwd())) # print current working directory
    print("Container size: " + str(sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))) + " bytes") # get folder size
    print("Container file count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)]))) # get amount of files in container folder
    print("Container contents: " + str(os.listdir("."))) # list contents of the container
    print("Upload log database: " + log.name)
    
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

apiServer = ThreadingHTTPServer((v.SERVER, v.API_PORT), ReqHandler)

if v.SSL_STATUS == True: # check whether SSL is enabled or not
    apiServer.socket = ssl.wrap_socket (apiServer.socket,  # ssl is enabled
        keyfile="./key.pem",
        certfile='./cert.crt', server_side=True)
else:
    pass # ssl is disabled

try: # start the API
    prestart()
    print("Starting the server, quit with ^C\n")
    apiServer.serve_forever() # start API endpoint
except KeyboardInterrupt: # handle keyboard interrupt
    print("Stopping...")
    exit()        