from http.server import HTTPServer,SimpleHTTPRequestHandler
from socketserver import BaseServer
from threading import Thread
from socketserver import ThreadingMixIn
import ssl, json, os, sys

with open("./config.json", 'r') as config_file: # import the JSON config data
	data = json.load(config_file)

class v: # holds all of the variables from config.json
	SERVER = data["SERVER"]
	API_PORT = data["API_PORT"]
	WEB_PORT = data["WWW_PORT"]
	SSL_KEY = data["SSL_KEY"]
	SSL_CERT = data["SSL_CERT"]
	WEB_FOLDER = data["WWW_FOLDER"]
	apiURL = (str(SERVER) + ":" + str(API_PORT))
	webURL = (str(SERVER) + ":" + str(WEB_PORT))

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
httpServer = ThreadingHTTPServer((v.SERVER, v.WEB_PORT), SimpleHTTPRequestHandler)
httpServer.socket = ssl.wrap_socket(httpServer.socket, certfile=v.SSL_CERT, keyfile=v.SSL_KEY, server_side=True)

def prestart():
	os.chdir(data["WWW_FOLDER"]) # set current directory as set in the WWW variable
	print("Simple File Container front-end")
	print("URL: " + str(v.webURL)) # prints a url to the webserver
	print("WWW folder: " + str(os.getcwd())) # current directory
	print("WWW files: " + str(os.listdir("."))) # list files in current directory

try: # start the HTTP server
	prestart()
	print("Starting frontend HTTP server, stop with ^C \n")
	httpServer.serve_forever()
except KeyboardInterrupt: # handle keyboard interrupt
	print("Stopping...")
	exit()