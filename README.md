# Simple File Container
### A basic file uploader and host.
Each uploaded file is stored in the "container", which is just a fancy way of saying a folder.

`sfc_www.py` is responsible for presenting files and serving the landing page to viewers.  

The `sfc_api.py` program handles uploading files and storing them in the container.

# TODO
- Add support for more file types
- Add HTTPS support
- Add token support
- Add dedicated upload logging (currently using the built-in logging from http.server)

# Setup
1. Clone this repository to any folder on your computer.
2. Open the `config.json` file and configure the variables to your needs.
- Server IP or domain that the server will be accessible from. Default is `127.0.0.1`.
- Port that the normal website can be accessed from, for viewing files. Default is `80`.
- API port, that the endpoint will recieve files on. Default is `8080`.
- WWW folder, where the index files are stored. Default is `www/`.
- Container folder, where the uploaded files are stored. Default is `www/c`
- Maximum upload size, stored as bytes. Default is `10mb`.
3. `www/index.html` will need to be edited so you can input the IP to your instance for the cURL example on line 8.
4. Launch both of the Python files with sudo. The page can be accessed at the servers IP on port 80.