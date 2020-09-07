# Simple File Container
### A basic file uploader and host.
Each uploaded file is stored in the "container", which is just a fancy way of saying a folder.

```curl -d "FILE OR @DATA" -H "Token: YOUR_TOKEN" -X POST http://"YOUR IP/DOMAIN":1024```  
[API documentation](https://github.com/SkryptKiddie/sfc/wiki/API)

# TODO
[Trello board](https://trello.com/b/tgSc5i7i/simple-file-container)
- Add support for ratelimiting API requests.

# Quick setup
1. Clone this repository to any folder on your computer.
2. Run `pip3 install -r requirements.txt`
3. Edit config.json using [this wiki as a guide](https://github.com/SkryptKiddie/sfc/wiki/Configuration).
4. Edit the template cURL command on`www/index.html` to reflect your instance settings.
5. Launch both of the Python files with sudo privileges. The page can be accessed at the servers IP on the specified web port. If your SSL key requires a password, you will be prompted to input it when you start each program.

# Supported mimetypes out of the box
- text/plain
- image/png
- image/jpeg
- image/gif
- audio/webm

## How do I disable SSL?
If for some reason, you'd like to disable SSL support, follow these instructions:  
1. Comment out line 23 in `sfc_www.py`.
2. Comment out line 156 in `sfc_api.py`.
3. Change `WWW_PORT` from 443 to 80 in `config.json`.

## I'm getting "Connection Refused" errors by my browser
Make sure your SSL keys are configured properly, and that you're visiting the correct site, which should be `https://127.0.0.1:443`, replacing 127.0.0.1 with the IP of your server.

## Can I add new features?
Sure! Just make a pull request and describe what you're adding and I will take a look.