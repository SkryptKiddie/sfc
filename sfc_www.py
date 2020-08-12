import http, os, sys, json # simple file container front-end website
from http.server import HTTPServer, CGIHTTPRequestHandler # tested on python 3.8.5

with open("./config.json", 'r') as config_file: # import the JSON config data
	data = json.load(config_file)

address=(str(data["SERVER"]), data["WWW_PORT"]) # combined variables for httpServer
serverURL=("http://"+str(data["SERVER"])+":"+(str(data["WWW_PORT"]))) # prettyprint the http server URL
httpServer = HTTPServer(server_address=(data["SERVER"], data["WWW_PORT"]), RequestHandlerClass=CGIHTTPRequestHandler) # httpServer

def prestart():
	os.chdir(data["WWW_FOLDER"]) # set current directory as set in the WWW variable
	print("Simple File Container front-end")
	print("URL: " + str(serverURL)) # prints a url to the webserver
	print("WWW folder: " + str(os.getcwd())) # current directory
	print("WWW files: " + str(os.listdir("."))) # list files in current directory

try:
	prestart()
	print("Starting frontend HTTP server, stop with ^C \n")
	httpServer.serve_forever()
except KeyboardInterrupt: # handle keyboard interrupt
	print("Stopping...")
	exit()