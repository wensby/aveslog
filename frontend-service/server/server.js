const express = require('express');
const axios = require('axios');

axios.defaults.baseURL = 'http://api-service:3002';

const app = express();
app.use(express.json())

const port = process.env.PORT || 3003;
app.set("port", port);

// Serve static assets in production
if (process.env.NODE_ENV === 'production') {
  const hashedFilePathPattern = new RegExp('\\.[0-9a-f]{8}\\.');

  app.use(express.static('client/build', {
    etag: true,
    lastModified: true,
    setHeaders: function (res, path) {
      if (hashedFilePathPattern.test(path)) {
        res.setHeader('Cache-Control', 'max-age=31536000');
      }
      else {
        res.setHeader('Cache-Control', 'no-cache');
      }
    },
  }));
}

app.use('/api/authentication', require('./authentication.js'));
app.use('/api/locales', require('./locales.js'));
app.use('/api/account', require('./account.js'));
app.use('/api/birds', require('./birds.js'));
app.use('/api/birders', require('./birders.js'));
app.use('/api/birder-connections', require('./birderConnections.js'));
app.use('/api/search', require('./search.js'));

app.post('/api/authentication/refresh-token', async (req, res) => {
  axios.post('/authentication/refresh-token', {}, {
    params: {
      username: req.query.username,
      password: req.query.password,
    }
  }).then(response => {
    res.status(response.status);
    res.json(response.data);
  }).catch(error => {
    if (error.response) {
      console.log(error.response.status);
      res.status(error.response.status);
      res.json({});
    }
  });
});

app.delete('/api/authentication/refresh-token/:id', (req, res) => {
  axios.delete(`authentication/refresh-token/${req.params.id}`, {
    headers: {
      accessToken: req.header('accessToken')
    }
  }).then(response => {
    res.status(response.status);
    res.json(response.data);
  }).catch(error => {
    if (error.response) {
      console.log(error.response.status);
      res.status(error.response.status);
      res.json({});
    }
  })
});

app.post('/api/registration-requests', async (req, res) => {
  const response = await axios.post('/registration-requests', {
    email: req.body.email,
    locale: req.body.locale
  });
  res.status(response.status);
  res.json(response.data);
});

app.get('/api/registration-requests/:id', async (req, res) => {
  const response = await axios.get(`/registration-requests/${req.params.id}`);
  res.json(response.data);
});

app.get('/api/authentication/access-token', async (req, res) => {
  const response = await axios.get('/authentication/access-token', {
    headers: {
      refreshToken: req.header('refreshToken'),
    }
  });
  res.json(response.data);
});

app.post('/api/accounts', async (req, res) => {
  const response = await axios.post('/accounts', {
    token: req.body.token,
    username: req.body.username,
    password: req.body.password,
  });
  res.status(response.status);
  res.json(response.data);
});

app.get('/api/sightings', async (req, res) => {
  const response = await axios.get('/sightings', {
    params: {
      limit: '10'
    },
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.json(response.data);
});

app.post('/api/sightings', async (req, res) => {
  const response = await axios.post('/sightings', req.body, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.set('location', response.headers['location']);
  res.status(response.status);
  res.json(response.data);
});

app.get('/api/sightings/:id', async (req, res) => {
  const response = await axios.get(`/sightings/${req.params.id}`, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.json(response.data);
});

app.delete('/api/sightings/:id', async (req, res) => {
  const response = await axios.delete(`/sightings/${req.params.id}`, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.status(response.status);
  res.json(response.data);
});

app.get('/api/birders', async (req, res) => {
  const response = await axios.get('/birders', {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.json(response.data);
});

app.patch('/api/birders/:id', async (req, res) => {
  const response = await axios.patch(`/birders/${req.params.id}`, req.body, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.json(response.data);
});

app.post('/api/account/password', async (req, res) => {
  const response = await axios.post('/account/password', req.body, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.status(response.status);
  res.json(response.data);
});

app.get('/api/birders/:id', async (req, res) => {
  const response = await axios.get(`/birders/${req.params.id}`, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.set('cache-control', response.headers['cache-control']);
  res.json(response.data);
});

app.get('/api/birders/:id/sightings', async (req, res) => {
  const response = await axios.get(`/birders/${req.params.id}/sightings`, {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.json(response.data);
});

app.get('/api/account', async (req, res) => {
  const response = await axios.get('/account', {
    headers: {
      accessToken: req.header('accessToken'),
    }
  });
  res.json(response.data);
});

app.get('/api/birds/:id', async (req, res) => {
  const response = await axios.get(`/birds/${req.params.id}`, {
    params: {
      embed: 'commonNames',
    }
  });
  res.set('cache-control', response.headers['cache-control']);
  res.json(response.data);
});

app.get('/api/birds/:id/common-names', async (req, res) => {
  const response = await axios.get(`/birds/${req.params.id}/common-names`);
  res.set('cache-control', response.headers['cache-control']);
  res.json(response.data);
});

app.get('/api/birds/:id/statistics', async (req, res) => {
  const response = await axios.get(`/birds/${req.params.id}/statistics`);
  res.json(response.data);
});

// Handles any requests that don't match the ones above
if (process.env.NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    res.sendFile(__dirname + '/client/build/index.html');
  });
}

app.listen(port);
console.log('App is listening on port ' + port);
