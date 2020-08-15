# Simple File Container
### A basic file uploader and host.
Each uploaded file is stored in the "container", which is just a fancy way of saying a folder.

```curl -d "Your message here" -H "Token: YOUR_TOKEN" -X POST http://"YOUR IP/DOMAIN":8080```

`sfc_www.py` is responsible for presenting files and serving the landing page to viewers.  

The `sfc_api.py` program handles uploading files and storing them in the container.

`sfc_clean.py` can be used to delete all the contents of the container.

# TODO
- Add support for more file types
- Add HTTPS support (working on implementing)
- ~~Add token support~~
- ~~Add dedicated upload logging (currently using the built-in logging from http.server)~~

# Quick setup
1. Clone this repository to any folder on your computer.
2. Run `pip3 install -r requirements.txt`
3. Open the `config.json` file and edit the values as mentioned below:
- Server IP or domain that the server will be accessible from. Default is `127.0.0.1`.
- WWW Port that the normal website can be accessed from, for viewing files. Default is `80`.
- API port, that the port the endpoint will recieve files on. Default is `8080`.
- SSL status. This is a **work-in-progress** and currently doesn't work. Default is `False`. Also includes the SSL key and certificate pair. Currently blank.
- WWW folder. This is where the index files are stored. Default is `www/`.
- Container folder. This is where the uploaded files are stored. Default is `www/c`.
- Filename length for uploads, default is `6`.
- Maximum upload size, in bytes. Default is `10mb`.
- Upload token, adds a layer of protection against unwanted uploads. Default is `test_123`. Must be embedded in the HTTP request Headers like so: `"Token: test_123"`.
- Upload log databse. Logs all of the successful uploads and stores the request time, filename, origin IP and token. Default is `log.db`.
4. Edit the template cURL command on`www/index.html` to reflect your instance settings.
5. Launch both of the Python files with sudo privileges. The page can be accessed at the servers IP on port 80.