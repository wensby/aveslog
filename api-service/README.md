Aveslog API v0
===============================================================================

## Overview

### Current version

Since this API is still under heavy development, this version of the API is
extremely volatile and there are no guarantees to consistency or functionality.
By default, all requests to https://api.aveslog.com will use the v0 routes. For
explicit use, just prefix all routes with 'v0/'.

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
404 Not Found

{
  "message": "Not Found"
}
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

