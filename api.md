# API
## Upload a file
```curl -d "Your message here" -H "Token: YOUR_TOKEN" -X POST http://"YOUR IP/DOMAIN":8080```

POST request to the server on port 8080 with the following header `("Token": "TOKEN_HERE")`
and the text to be uploaded in the body.  

### Successful request
If all conditions are met, the API will respond with `200 File Uploaded` and response body will have the URL to the file and a unique ID for the upload. The response headers will have `("Uploaded": "True")`.  

### Unsuccessful request
- If the file exceeds the upload limit (default is 10mb), the API will respond with 431 Request Header Fields Too Large and a `(Uploaded: False)` header.
- If an incorrect token is provided, the API will respond with 401 Unauthorised and a `(Uploaded: False)` header.
- If an unexpected error occurs, the API will respond with 500 Internal Server Error and a `(Uploaded: False)` header.

## Delete a file
```curl -H 'Token: TOKEN_HERE' -H 'File: FILENAME_HERE.txt' http://"YOUR IP/DOMAIN":8080```

DELETE request to the API on port 8080 with 2 headers:
- Upload token
- The file name, including the .txt extension.

### Successful request
If all conditions are met, the server will respond with 200 File Deleted and a `(Deleted: True)` header.

### Unsuccessful request
- If no token is provided, the API will respond with a 401 Unauthorised and a `(Deleted: True)` header.  
-  If the requested file can't be found, the API will respond with 404 File Not Found and a `(Deleted: True)` header. 
- If an unknown error occurs, the server will respond with 500 Internal Server Error and and a `(Deleted: True)` header. 

## Notes
- GET requests to the API will be met with 405 Method Not Allowed.