There are many ways to send data inside a request.

## 1. Request/Query Parameters
If you want to send data in the URL, you can use request/query parameters. This is the most common way to send data to a server.
The data is appended to the URL after a ?. If there are multiple parameters, they are separated by &.
This data is not sent in the body of the request, but in the URL.
This data is not encrypted.
The query parameters are not the part of the path/endpoint, but the part of the URL.

When the backend wants a few query parameters, but the user doesn't send all of them, the backend can still process the request.

Example:
If you want to send the following data:
```json
{
  "key": "value",
  "key2": "value2"
}
```
Then the URL will be:
```/test?key=value&key2=value2```

A real world example is the Google Search API.
```https://www.google.com/search?q=cats```
The data is sent in the URL after a ?.
The data is not sent in the body of the request, but in the URL.
The data is not encrypted.
The query parameters are not the part of the path/endpoint, but the part of the URL.


## 2. Path Parameters
If you want to send data in the path of the URL, you can use path parameters.
The data is appended to the URL after a /. If there are multiple parameters, they are separated by /.
The data is not sent in the body of the request, but in the URL.
The data is not encrypted.
The path parameters are the part of the path/endpoint, but not the part of the URL.

Example:
If you want to send the following data:
```json
{
  "key": "value",
  "key2": "value2"
}
```
Then the URL will be:
```/test/value/value2```

A real world example is the GitHub API.
```https://api.github.com/users/octocat/repos```
The data is sent in the path of the URL after a /.
The data is not sent in the body of the request, but in the URL.
The data is not encrypted.
The path parameters are the part of the path/endpoint, but not the part of the URL.

## 3. Request Body
If you want to send data in the body of the request, you can use the request body.
This is the most common way to send data to a server.
The data is sent in the body of the request.
The data is not encrypted.
The request body is the part of the request, but not the part of the URL.

Example:
If you want to send the following data:
```json
{
  "key": "value",
  "key2": "value2"
}
```
Then the request body will be:
```json
{
  "key": "value",
  "key2": "value2"
}
```
The data is sent in the body of the request.
The data is not encrypted.
The request body is the part of the request, but not the part of the URL.

## 4. Headers
If you want to send data in the headers of the request, you can use headers.
The data is sent in the headers of the request.
The data is not encrypted.
The headers are the part of the request, but not the part of the URL.

Example:
If you want to send the following data:
```json
{
  "key": "value",
  "key2": "value2"
}
```
Then the headers will be:
```
{
  "key": "value",
  "key2": "value2"
}
```
The data is sent in the headers of the request.
The data is not encrypted.
The headers are the part of the request, but not the part of the URL.

A real world example is the GitHub API.
```
Authorization: Bearer ghp_yourTokenHere
Accept: application/vnd.github+json
```
The token is sent in the `Authorization` header, not in the URL.
The data is not sent in the body of the request, but in the headers.
The data is not encrypted.
The headers are the part of the request, but not the part of the URL.


