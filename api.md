# API
## Upload a file
```curl -d "TEXT OR @DATA" -H "Token: YOUR_TOKEN" -X POST "YOUR IP/DOMAIN":1024```

POST request to the server on port 1024 with the following headers:
- Upload token ("Token": "TOKEN_HERE")
- File type ("Content-Type": "mime/type") (optional)
- File to be uploaded (text, image, etc.)

### Successful request
If all conditions are met, the API will respond with `200 File Uploaded` and response body will have the URL to the file and a unique ID for the upload. The response headers will have `("Uploaded": "True")`.  

### Unsuccessful request
- If the file exceeds the upload limit (default is 10mb), the API will respond with 431 Request Header Fields Too Large and a `(Uploaded: False)` header.
- If an incorrect token is provided, the API will respond with 401 Unauthorised and a `(Uploaded: False)` header.
- If the file type is invalid, the API will respond with a 500 Internal Server Error and a `(Uploaded: False)` header. (Will be given it's own error code eventually)
- If an unexpected error occurs, the API will respond with 500 Internal Server Error and a `(Uploaded: False)` header.

## Delete a file
```curl -H "Token: YOUR_TOKEN" -H "File: FILENAME_HERE" "YOUR IP/DOMAIN":1024```

DELETE request to the API on port 1024 with 2 headers:
- Upload token
- The file name, including the file extension.

### Successful request
If all conditions are met, the server will respond with 200 File Deleted and a `(Deleted: True)` header.

### Unsuccessful request
- If no token is provided, the API will respond with a 401 Unauthorised and a `(Deleted: True)` header.  
-  If the requested file can't be found, the API will respond with 404 File Not Found and a `(Deleted: True)` header. 
- If an unknown error occurs, the server will respond with 500 Internal Server Error and and a `(Deleted: True)` header. 

## Notes
- GET requests to the API will be met with 405 Method Not Allowed.