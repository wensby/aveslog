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


## Errors

Client errors are returned with HTTP Status Code in the 400s, while server
errors are returned in the 500s. A typical error response looks like the
following:

```
Status: 400 BAD REQUEST

{
  "code": 1,
  "message": "Email invalid"
}
```

When trying to get a resource that isn't there, the API will naturally respond
with:

```
Status: 404 Not Found

{
  "message": "Not Found"
}
```

### Error Codes

| Error code | Description |
|---|---|
| 1 | Provided registration email didn't fit the required format. See the section on Registration. | 
| 2 | Provided registration email is already associated with a registered account. |
| 3 | Provided username already associated with a registered account. |
| 4 | Provided credentials incorrect. This could mean either the username or password. |
| 5 | Request requires authorization in form of a valid access token. |
| 6 | Provided email is not associated with any account. |
| 7 | Provided old password incorrect. |
| 8 | Provided access token invalid. |
| 9 | Provided access token expired. |
| 10 | Provided new password invalid. |
| 11 | Account associated with the access token provided no longer available. |
| 12 | Rate limit exceeded. Check response header X-Rate-Limit-Reset for how many seconds remains until the next window. |
| 13 | Registration request token used when creating a new account is invalid or not associated with an existing registration request. |
| 14 | One or more of the provided parameters to the request failed a validation. See provided errors for more detailed information. |
| 15 | Username does not follow required format. |
| 16 | Password does not follow required format. |
| 17 | Provided locale code not one of the allowed codes. |


## Authentication

### Create Refresh Token

In order to obtain a short-lived access token required to access and modify
certain resources, you first need a refresh token.

```
POST /authentication/refresh-token?username={username}&password={password}
```

**Response**

```
Status: 201 CREATED

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

**Response**

```
Status: 204 NO CONTENT
```

### Get Access Token

```
GET /authentication/access-token
```

**Required Headers**

`refreshToken: {refreshTokenJwt}`

**Response**

```
Status: 200 OK

{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "expiresIn": 1799
}
```

**Possible Errors**

`Status: 401 UNAUTHORIZED` When refresh token used to get access token is either
invalid, expired, or revoked.

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

**Response**

```
Status: 200 OK
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

**Response**

```
Status: 200 OK
```


## Birds

### Get single bird

```
GET /birds/:bird
```

**Response**

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

**Embeddable fields**

`commonNames`

### Get bird statistics

```
GET /birds/:bird/statistics
```

**Response**

```
Status: 200 OK

{
  "sightingsCount": 2,
  "birdersCount": 1
}
```

### Get single bird's common name

```
GET /birds/:bird/common-names/:id
```

**Response**

```
{
  "id": 1,
  "locale": "sv",
  "name": "Skata"
}
```

### Get bird's common names

```
GET /birds/:bird/common-names
```

**Response**

```
{
  "items": [
    {
      "id": 1,
      "locale": "sv",
      "name": "Skata"
    },
    {
      "id": 2,
      "locale": "en",
      "name": "Eurasian Magpie"
    }
  ]
}
```

**Filters**

`locale`
example
`/birds/pica-pica/common-names?locale=sv`

### Add bird common name

This endpoint requires that the authenticated account hava a role with required
permission.

```
POST /birds/:bird/common-names
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Post Data Example**

```
{
  "locale": "sv",
  "name": "Skata"
}
```

**Response**

```
Status: 201 CREATED
```

## Sightings

### List birder's sightings

```
GET /birders/:id/sightings
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
{
  "items": [
    {
      "id": 4,
      "birderId": 8,
      "birdId": "pica-pica",
      "date": "2019-11-19",
      "time": "20:17:00"
      "position": {
        "lat": 47.240055,
        "lon": 2.2783327
      }
    }
  ],
  "hasMore": false
}
```

### List all sightings

```
GET /sightings
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 200 OK

{
  "items": [
    {
      "id": 4,
      "birderId": 8,
      "birdId": "pica-pica",
      "date": "2019-11-19",
      "time": "20:17:00",
      "position": {
        "lat": 47.240055,
        "lon": 2.2783327
      }
    },
    {
      "id": 15,
      "birderId": 16,
      "birdId": "passer-domesticus",
      "date": "2019-11-19"
    }
  ],
  "hasMore": false
}
```

### Get sighting

```
GET /sightings/:id
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 200 OK

{
  "id": 4,
  "birderId": 8,
  "birdId": "pica-pica",
  "date": "2019-11-19",
  "time": "20:17:00",
  "position": {
    "name': "La Prinquette, Bourges, Cher, Centre-Val de Loire, France métropolitaine, France",
    "lat": 47.240055,
    "lon": 2.2783327
  },
}
```

### Delete sighting

```
DELETE /sightings/:id
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 204 NO CONTENT
```

### Create sighting

```
POST /sightings
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Post Data Example**

```
{
  "birder": {
    "id": 4
  },
  "bird": {
    "binomialName": "Pica pica"
  },
  "date": "2019-11-19",
  "time": "20:35:00",
  "position": {
    "lat": 47.240055,
    "lon": 2.2783327
  }
}
```

**Response**

```
Status: 201 CREATED
Location: /sightings/8
```

## Account

### Get single account

```
GET /accounts/:username
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 200 OK

{
  "id": 4,
  "username": "kennybostick",
  "birder": {
    "id": 8,
    "name": "kennybostick"
  }
}
```

### Create Account

In order to create an account, you first need to have obtained a registration
request token. This token is emailed to you by creating a new registration
request providing your email address.

```
POST /accounts

{
  "token": "{registration-token}"
  "username": "kennybostick",
  "password": "birder-no-1"
}
```

**Response**

The response from completing a registration is the created account resource.

```
Status: 201 CREATED

{
  "id": 4,
  "username": "kennybostick",
  "email": "kenny.bostick@mail.com",
  "birder": {
    "id": 8,
    "name": "kennybostick"
  }
}
```

Upon a successful account creation, the registration request resource associated
with the token used will be consumed and deleted.

### Get Authenticated Account

```
GET /account
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 200 OK

{
  "id": 4,
  "username": "kennybostick",
  "email": "kenny.bostick@mail.com",
  "birder": {
    "id": 8,
    "name": "kennybostick"
  }
}
```

### Update account password

Updating the authenticated account's password will also result in all refresh
tokens associated with this account being revoked.

```
POST /account/password

{
  "oldPassword": "birder-no-1",
  "newPassword": "still-birder-no-1"
}
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 204 NO CONTENT
```

### Get Accounts

```
GET /accounts
```

**Required Headers**

`accessToken: {accessTokenJwt}`

**Response**

```
Status: 200 OK

{
  "items": [
    {
      "username": "kennybostick",
      "birderId": 4
    },
    {
      "username": "bradharris",
      "birderId": 8
    },
    {
      "username": "stupreissler",
      "birderId": 15
    }
  ]
}
```

## Locales

### Get locales

```
GET /locales
```

**Response**

```
Status: 200 OK

{
  "items": ['sv', 'en']
}
```


## Registration Requests

Registering a new account is a 2 step process. First, you create a registration
request by provide your email address. Upon a success, this will trigger an 
email to be sent containing a unique registration token 
`:registration-request-token`. Once you've acquired this token, you can use this
token perform your final registration request.

### Create Registration Request

```
POST /registration-requests

{
  "email": "kenny.bostick@mail.com"
}
```

The email address needs to follow the following format:

```regexp
^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$
```

**Response**

```
Status: 201 CREATED
```

### Get Registration Request

It could be useful to get the registration request, and email address,
associated with a specific registration token, before actually completing the
registration.

```
GET /registration-requests/:registration-request-token
```

**Response**

```
Status: 200 OK

{
  "email": "hulot@mail.com"
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
