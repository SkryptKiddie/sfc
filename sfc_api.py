import http, os, sys, json, pathlib, ssl # simple file storage backend
import random, string, os.path, time # tested on python 3.8.5
from io import BytesIO
from threading import Thread
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from tinydb import TinyDB, Query

with open('./config.json', 'r') as config_file:
    data = json.load(config_file)

class v: # holds all of the variables from config.json
    SERVER = data["SERVER"]
    API_PORT = data["API_PORT"]
    WEB_PORT = data["WWW_PORT"]
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

log = TinyDB(v.UPLOAD_DB, indent=4) # upload logging database
file = Query()

def generateFn(length): # sourced from https://pynative.com/python-generate-random-string/
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return str(result_str) # return the filename

def generateGuid(): # generate file hex in case the file is renamed or something
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(20))

class ReqHandler(BaseHTTPRequestHandler): # handle accidental GET requests to the backend
    def do_GET(self):
        self.send_error(405, message="This endpoint only accepts POST requests")
        self.end_headers()
        self.flush_headers()

    def do_POST(self): # handle incoming POST requests
        content_length = int(self.headers["Content-Length"])
        uploader_token = str(self.headers["Token"])
        content_type = str(self.headers["Content-Type"])
        body = self.rfile.read(content_length)
        response = BytesIO()
        if str(uploader_token) == v.UPLOAD_TOKEN: # checks upload token
            if content_length < v.MAX_UPLOAD: # checks file size
                try: # try to upload the file
                    newFileName = (str(generateFn(v.FILENAME_LENGTH)) + ".txt")
                    newFileGuid = generateGuid()
                    self.send_response(200, message="Upload recieved")
                    self.send_header("Content-type", "text/plain")
                    self.send_header("Upload-ID", str(newFileGuid))
                    self.send_header("Uploaded", "True")
                    with open(str(newFileName), "w") as newUpload: # sourced from https://www.geeksforgeeks.org/create-an-empty-file-using-python/
                        newUpload.write(str(body)[2:-1]) # store the string that we recieved
                        pass
                    try: # attempt to log the upload in the database
                        log.insert(
                        {"upload_time": str(self.log_date_time_string()), 
                        "uploader_ip": str(self.address_string()),
                        "guid": str(newFileGuid),
                        "token": str(v.UPLOAD_TOKEN), 
                        "filename": str(newFileName),
                        "filetype": str(content_type)})
                    except: # traceback incase the log file isn't available or something
                        stats = os.stat(newFileName)
                        print(str(self.log_date_time_string()) + 
                        " | IP: " + str(self.address_string()) + 
                        " | GUID: " + str(newFileGuid) +
                        " | File: " + str(newFileName) + 
                        " | Size: " + str(stats.st_size) + " bytes." + 
                        " | File count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)])))

                    link = str.encode(str(v.webURL) + "/c/" + str(newFileName) + "\n")
                    response.write(link) # send the URL to the file
                    #response.write(str.encode((newFileGuid)))
                    self.wfile.write(response.getvalue())
                    self.end_headers()
                    self.flush_headers()

                except: # in case something happens, tell the client and log it
                    print("An error occured while trying to upload.")
                    self.send_error(500, message="An error occured while trying to upload your file, please try again later")
                    self.send_header("Uploaded", "False")
                    self.end_headers()
                    self.flush_headers()

            else: # error if file too big
                print("Rejected large upload.")
                self.send_error(431, message="File size exceeds limit") # 431 Request Header Fields Too Large
                self.send_header("Uploaded", "False")
                self.end_headers()
                self.flush_headers()

        else: # error if incorrect token
            print("Rejected unauthorised uploader.")
            self.send_error(401, message="Bad Token") # 401 Unauthorised
            self.send_header("Uploaded", "False")
            self.end_headers()
            self.flush_headers()

    def do_DELETE(self): # handle DELETE requests
        uploader_token = str(self.headers["Token"])
        delFile = str(self.headers["File"])
        if str(uploader_token) == v.UPLOAD_TOKEN:
            reqFile = pathlib.Path(delFile)
            if reqFile.exists():
                log.remove(file.filename == delFile)
                os.remove(delFile)
                self.send_response(200, message="File Deleted")
                self.send_header("Deleted", "True")
                self.end_headers()
                self.flush_headers()
            else:
                self.send_response(404, message="File Not Found")
                self.send_header("Deleted", "False")
                self.end_headers()
                self.flush_headers()
        else:
            self.send_error(401, message="Bad Token") # 401 Unauthorised
            self.send_header("Deleted", "False")
            self.end_headers()
            self.flush_headers()

# runtime
def prestart():
    os.chdir(v.CONTAINER_FOLDER) # set current directory as set in the WWW variable
    print("Simple File Container API")
    print("URL: " + str(v.apiURL))
    print("Current container: " + str(os.getcwd())) # print current working directory
    print("Container size: " + str(sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))) + " bytes") # get folder size
    print("Container file count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)]))) # get amount of files in container folder
    print("Upload log database: " + log.name)
    
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
apiServer = ThreadingHTTPServer((v.SERVER, v.API_PORT), BaseHTTPRequestHandler, ReqHandler)
apiServer.socket = ssl.wrap_socket(apiServer.socket, certfile=v.SSL_CERT, keyfile=v.SSL_KEY, server_side=True)

try: # start the API
    prestart()
    print("Starting the server, quit with ^C\n")
    apiServer.serve_forever() # start API endpoint
except KeyboardInterrupt: # handle keyboard interrupt
    print("Stopping...")
    exit()