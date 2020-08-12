import http, os, sys, json # simple file storage backend
import random, string, os.path, time # tested on python 3.8.5
from http.server import HTTPServer, CGIHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

with open('./config.json', 'r') as config_file:
    data = json.load(config_file)

SERVER = data["SERVER"]
API_PORT = data["API_PORT"]
WEB_PORT = data["WWW_PORT"]
WEB_FOLDER = data["WWW_FOLDER"]
CONTAINER_FOLDER = data["WWW_FOLDER"] + "/" + data["CONTAINER_FOLDER"]
MAX_UPLOAD = data["MAX_UPLOAD_SIZE"]
UPLOAD_TOKEN = data["UPLOAD_TOKEN"]

apiURL = ("http://" + str(SERVER) + ":" + str(API_PORT))
webURL = ("http://" + str(SERVER) + ":" + str(WEB_PORT))

def filenameGenerator(length): # sourced from https://pynative.com/python-generate-random-string/
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return str(result_str) # return the filename

class ReqHandler(BaseHTTPRequestHandler): # handle accidental GET requests to the backend
    def do_GET(self):
        self.send_response(405)
        self.end_headers()

    def do_POST(self): # handle incoming POST requests
        content_length = int(self.headers['Content-Length'])
        uploader_token = str(self.headers['Token'])
        body = self.rfile.read(content_length)
        if content_length > MAX_UPLOAD: # handle files that are too big, https://stackoverflow.com/questions/28217869/python-basehttpserver-file-upload-with-maxfile-size
            print("Rejected large upload.")
            self.send_response(431) # 431 Request Header Fields Too Large
            self.end_headers()
        else:
            if str(uploader_token) == UPLOAD_TOKEN: # checks for uploader token
                self.send_response(200) 
                self.send_header('Last-Modified', self.date_time_string(time.time()))
                newFileName=(str(filenameGenerator(6)) + ".txt")
                with open(str(newFileName), 'w') as newUpload: # sourced from https://www.geeksforgeeks.org/create-an-empty-file-using-python/
                    newUpload.write(str(body)) # store the string that we recieved
                    pass
                stats = os.stat(newFileName) # print stats for the newly uploaded file
                print("New file created, " + str(newFileName) + " and is " + str(stats.st_size) + " bytes. File count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)])))
                print(str(webURL) + "/c/" + newFileName) # prints the URL to the file
                response = BytesIO() 
                response.write(b"File uploaded!") # response back to the client
                #response.write(str(webURL) + "/c/" + newFileName)
                self.wfile.write(response.getvalue())
                self.end_headers() # close the connection
            else:
                response = BytesIO()
                print("Rejected unauthorised uploader.")
                self.send_response(403) # 403 Forbidden
                response.write(b"A token required to upload.")
                self.end_headers()

# runtime
def prestart():
    os.chdir(CONTAINER_FOLDER) # set current directory as set in the WWW variable
    print("Simple File Container API")
    print("URL: " + str(apiURL))
    print("Container: " + str(os.getcwd())) # print current working directory
    print("Container size: " + str(sum(os.path.getsize(f) for f in os.listdir(".") if os.path.isfile(f))) + " bytes") # get folder size
    print("Container file count: " + str(len([name for name in os.listdir(".") if os.path.isfile(name)]))) # get amount of files in container folder
    print("Container contents: " + str(os.listdir("."))) # list contents of the container

try:
    prestart()
    print("Starting the server, quit with ^C\n")
    apiServer = HTTPServer((SERVER, API_PORT), ReqHandler)
    apiServer.serve_forever() # start API endpoint
except KeyboardInterrupt: # handle keyboard interrupt
    print("Stopping...")
    exit()        