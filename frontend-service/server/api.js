var express = require('express');
var router = express.Router();
const axios = require('axios');
const { setupAxios } = require('./middleware.js');

axios.defaults.baseURL = 'http://api-service:3002';

router.use('/', setupAxios);

router.use('/authentication', require('./authentication.js'));
router.use('/locales', require('./locales.js'));
router.use('/account', require('./account.js'));
router.use('/birds', require('./birds.js'));
router.use('/bird-pages', require('./birdPages.js'));
router.use('/birders', require('./birders.js'));
router.use('/birder-page', require('./birderProfile.js'));
router.use('/birder-connections', require('./birderConnections.js'));
router.use('/search', require('./search.js'));

router.post('/authentication/refresh-token', async (req, res) => {
  req.axios.post('/authentication/refresh-token', {}, {
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

router.delete('/authentication/refresh-token/:id', (req, res) => {
  req.axios.delete(`authentication/refresh-token/${req.params.id}`)
  .then(response => {
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

router.post('/registration-requests', async (req, res) => {
  const response = await req.axios.post('/registration-requests', {
    email: req.body.email,
    locale: req.body.locale
  });
  res.status(response.status);
  res.json(response.data);
});

router.get('/registration-requests/:id', async (req, res) => {
  const response = await req.axios.get(`/registration-requests/${req.params.id}`);
  res.json(response.data);
});

router.get('/authentication/access-token', (req, res) => {
  req.axios.get('/authentication/access-token', {
    headers: {
      refreshToken: req.header('refreshToken'),
    }
  })
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    })
    .catch(error => {
      if (error.response) {
        res.status(error.response.status).end();
      }
    })

});

router.post('/accounts', async (req, res) => {
  const response = await req.axios.post('/accounts', {
    token: req.body.token,
    username: req.body.username,
    password: req.body.password,
  });
  res.status(response.status);
  res.json(response.data);
});

router.get('/sightings', async (req, res) => {
  const response = await req.axios.get('/sightings', {
    params: {
      limit: '10'
    }
  });
  res.json(response.data);
});

router.post('/sightings', async (req, res) => {
  const response = await req.axios.post('/sightings', req.body);
  res.set('location', response.headers['location']);
  res.status(response.status);
  res.json(response.data);
});

router.get('/sightings/:id', async (req, res) => {
  const response = await req.axios.get(`/sightings/${req.params.id}`);
  res.json(response.data);
});

router.delete('/sightings/:id', async (req, res) => {
  const response = await req.axios.delete(`/sightings/${req.params.id}`);
  res.status(response.status);
  res.json(response.data);
});

router.get('/birders', async (req, res) => {
  const response = await req.axios.get('/birders');
  res.json(response.data);
});

router.patch('/birders/:id', async (req, res) => {
  const response = await req.axios.patch(`/birders/${req.params.id}`);
  res.json(response.data);
});

router.post('/account/password', async (req, res) => {
  const response = await req.axios.post('/account/password', req.body);
  res.status(response.status);
  res.json(response.data);
});

router.get('/birders/:id', async (req, res) => {
  const response = await req.axios.get(`/birders/${req.params.id}`);
  res.set('cache-control', response.headers['cache-control']);
  res.json(response.data);
});

router.get('/birders/:id/sightings', async (req, res) => {
  const response = await req.axios.get(`/birders/${req.params.id}/sightings`);
  res.json(response.data);
});

router.get('/account', async (req, res) => {
  const response = await req.axios.get('/account');
  res.json(response.data);
});

router.get('/birds/:id', async (req, res) => {
  const response = await req.axios.get(`/birds/${req.params.id}`, {
    params: {
      embed: 'commonNames',
    }
  });
  res.set('cache-control', response.headers['cache-control']);
  res.json(response.data);
});

router.get('/birds/:id/common-names', async (req, res) => {
  const response = await req.axios.get(`/birds/${req.params.id}/common-names`);
  res.set('cache-control', response.headers['cache-control']);
  res.json(response.data);
});

router.get('/birds/:id/statistics', async (req, res) => {
  const response = await req.axios.get(`/birds/${req.params.id}/statistics`);
  res.json(response.data);
});

module.exports = router;
