Aveslog API v0
===============================================================================

## Overview

### Current version

Since this API is still under heavy development, this version of the API is
extremely volatile and there are no guarantees to consistency or functionality.
By default, all requests to https://api.aveslog.com will use the v0 routes. For
explicit use, just prefix all routes with 'v0/'.

### Pagination

Requests that return multiple items will be paginated to 30 items by default.
To specify a custom page size, use the parameter `page_size`, which will allow
page sizes for up to 100 items.

### Rate Limiting

The returned HTTP headers of any API request show your current rate limit
status:

```
curl -i https://api.aveslog.com/birds/pica-pica
HTTP/1.1 200 OK
Date: Sat, 09 Nov 2019 06:52:49 GMT
X-Rate-Limit-Limit: 100
X-Rate-Limit-Remaining: 99
X-Rate-Limit-Reset: 1
```

| Header Name            | Description                                             |
|------------------------|---------------------------------------------------------|
| X-Rate-Limit-Limit     | The number of allowed requests in the current period.   |
| X-Rate-Limit-Remaining | The number of remaining requests in the current period. |
| X-Rate-Limit-Reset     | The number of seconds left in the current period.       |


### Errors

When trying to get a resource that isn't there, the API will naturally respond
with:

```
Status: 404 Not Found

{
  "message": "Not Found"
}
```


## Authentication

### Account Registration

Registering a new account is a 2 step process. First, you provide your email 
address when creating a new registration resource.

#### Initiating New Account Registration

```
POST /authentication/registration

{
  "email": "kenny.bostick@mail.com"
}
```

#### Response

```
Status: 200 OK

{
  "status": "success"
}
```

Upon a success, this will trigger an email to be sent to this email address
containing a unique registration token `:registration-token`. Once you've
acquired this token, you can perform your final registration request using this
token.

#### Getting Registration

```
GET /authentication/registration/:registration-token
```

#### Response

```
Status: 200 OK

{
  "status": "success",
  "result": {
    "registration": {
      "email": "hulot@mail.com"
    }
  }
}
```

#### Completing a Registration

```
POST /authentication/registration/:registration-token

{
  "username": "kennybostick",
  "password": "birder-no-1"
}
```

#### Response

```
Status: 200 OK

{
  "status": "success",
  "message": "Registration successful"
}
```

### Create Refresh Token

In order to obtain a short-lived access token required to access and modify certain
resources, you first need a refresh token.

```
POST /authentication/refresh-token?username={username}&password={password}
```

#### Response

```
Status: 200 OK

{
  "id": 4,
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "expirationDate": "2020-02-10T06:21:45.414236"
}
```

### Delete Refresh Token

```
DELETE /authentication/refresh-token/:id
```

**Required Headers**

`accessToken: {accessTokenJwt}`

#### Response

```
Status: 204 NO CONTENT
```

### Get Access Token

```
GET /authentication/access-token
```

**Required Headers**

`refreshToken: {refreshTokenJwt}`

#### Response

```
Status: 200 OK

{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "expiresIn": 1799
}
```

### Password Reset

Just like registering a new account, resetting a password is a 2-step process.
First, you initiate your password reset by providing an email associated with
the account for which the password should get reset.

#### Initiate Password Reset

```
POST /authentication/password-reset

{
  "email": "kenny.bostick@mail.com"
}
```

#### Response

```
Status: 200 OK

{
  "status": "success",
  "message": "Password reset link sent to e-mail"
}
```

Upon a success, this will trigger an email to be sent to this email address
containing a unique password reset token `:password-reset-token`. Once you've
acquired this token, you can perform your final password reset using this token.

#### Completing Password Reset

```
POST /authentication/password-reset/:password-reset-token

{
  "password": "still-birder-no-1"
}
```

#### Response

```
Status: 200 OK
{
  "status": "success",
  "message": "Password reset successfully"
}
```

### Update Password

```
POST /authentication/password
```

**Required Headers**

`accessToken: {accessTokenJwt}`

#### Response

```
Status: 204 NO CONTENT
```


## Birds

### Get Bird

```
GET /birds/:bird
```

#### Response

```
Status: 200 OK

{
  "id": "pica-pica",
  "binomialName": "Pica pica",
  "thumbnail": {
    "url": "https://api.aveslog.com/static/image/bird/pica-pica-thumb.jpg",
    "credit": "Anna Larsson",
  },
  "cover": {
    "url": "https://api.aveslog.com/static/image/bird/pica-pica-thumb.jpg",
    "credit": "Anna Larsson",
  }
}
```


## Search

The Search API helps you search for the specific item you want to find. Each
item returned in a search response will have an extra field 'score', signaling
how well it matched the search query. Items scoring 0 will not be returned.

### Search Birds

```
GET /search/birds
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| q | string | **Required.** |
| embed | string | Optional comma separated list of fields to be included in each result item. Supported field is: thumbnail. |

#### Response

```
Status: 200 OK

{
  "items": [
    {
      "binomialName": "Pica pica",
      "id": "pica-pica",
      "score": 1.0,
    }
  ]
}
```
