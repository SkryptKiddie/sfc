# Simple File Container
### A basic file uploader and host.
Each uploaded file is stored in the "container", which is just a fancy way of saying a folder.

```curl -d "FILE OR @DATA" -H "Token: YOUR_TOKEN" -X POST http://"YOUR IP/DOMAIN":1024```

`sfc_www.py` is responsible for presenting files and serving the landing page to viewers.  

The `sfc_api.py` program handles uploading files and storing them in the container.

`sfc_clean.py` can be used to delete all the contents of the container.

# TODO
- Add support for ratelimiting API requests.
- ~~Add support for more file types~~
- ~~Add HTTPS support (working on implementing)~~
- ~~Add token support~~
- ~~Add dedicated upload logging (currently using the built-in logging from http.server)~~

# Quick setup
1. Clone this repository to any folder on your computer.
2. Run `pip3 install -r requirements.txt`
3. Open the `config.json` file and edit the values as mentioned below:
- Server IP or domain that the server will be accessible from. Default is `0.0.0.0`.
- WWW Port that the normal website can be accessed from, for viewing files. Default is `443`.
- API port, that the port the endpoint will recieve files on. Default is `1024`.
- Filepath to both your SSL key and SSL certificate. Until I can figure out how to make HTTPS support optional, you will have to manually disable it by commenting out the `httpServer.socket` and `apiServer.socket` lines.
- WWW folder. This is where the index files are stored. Default is `www/`.
- Container folder. This is where the uploaded files are stored. Default is `www/c`.
- Filename length for uploads, default is `6`.
- Maximum upload size, in bytes. Default is `10mb`.
- Upload log databse. Logs all of the successful uploads and stores the request time, filename, origin IP and token. Default is `log.db`.
4. Edit the `users.json` file and edit the default tokens for uploading. By default, there are 3 users.
5. Edit the template cURL command on`www/index.html` to reflect your instance settings.
6. Launch both of the Python files with sudo privileges. The page can be accessed at the servers IP on the specified web port. If your SSL key requires a password, you will be prompted to input it when you start each program.

# Supported mimetypes out of the box
- text/plain
- image/png
- image/jpeg
- image/gif
- audio/webm

# Troubleshooting  
## How do I upload something?
Refer to the `api.md` file located in this repository.  

## How do I disable SSL?
If for some reason, you'd like to disable SSL support, follow these instructions:  
1. Comment out line 23 in `sfc_www.py`.
2. Comment out line 144 in `sfc_api.py`.
3. Change `WWW_PORT` from 443 to 80 in `config.json`.

## I'm getting "Connection Refused" errors by my browser
Make sure your SSL keys are configured properly, and that you're visiting the correct site, which should be `https://127.0.0.1:443`, replacing 127.0.0.1 with the IP of your server.

## Can I add new features?
Sure! Just make a pull request and describe what you're adding and I will take a look.