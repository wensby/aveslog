Aveslog API v0
===============================================================================

## Overview

### Current version

Since this API is still under heavy development, this version of the API is
extremely volatile and there are no guarantees to consistency or functionality.
By default, all requests to https://api.aveslog.com will use the v0 routes. For
explicit use, just prefix all routes with 'v0/'.

## Birds

### Get Bird

```
GET /birds/:bird
```

#### Response

```
Status: 200 OK

{
  "binomialName": "Pica pica",
  "coverUrl": "https://api.aveslog.com/static/image/bird/pica-pica-thumb.jpg",
  "thumbnailCredit": "Anna Larsson",
  "thumbnailUrl": "https://api.aveslog.com/static/image/bird/pica-pica-thumb.jpg"
}
```

The bird identifier can either be the birds' numerical ID (eg. 6871), or its
binomial name with dashes instead of spaces (pica-pica).

