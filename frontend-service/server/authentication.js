var express = require('express');
var router = express.Router();

router.post('/tokens', async (req, res) => {
  try {
    const refreshTokenResponse = await req.axios.post('/authentication/refresh-token', {}, {
      params: {
        username: req.body.username,
        password: req.body.password,
      }
    });
    const refreshToken = refreshTokenResponse.data;
    const accessTokenResponse = await req.axios.get('/authentication/access-token', {
      headers: { refreshToken: refreshToken.refreshToken }
    });
    const accessToken = accessTokenResponse.data;
    res.json({ refreshToken, accessToken });
  } catch (error) {
    console.log(error);
    res.status(401).end();
  }
});

router.post('/access-token', (req, res) => {
  req.axios.get('/authentication/access-token', {
    headers: {
      refreshToken: req.body.refreshToken,
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

router.post('/refresh-token', async (req, res) => {
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

router.delete('/refresh-token/:id', (req, res) => {
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

router.post('/credentials-recovery', (req, res) => {
  req.axios.post('/authentication/credentials-recovery', req.body)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    })
    .catch(error => {
      if (error.response) {
        res.status(error.response.status);
        res.json(error.response.data);
      }
    });
});

router.post('/password-reset/:token', (req, res) => {
  req.axios.post(`/authentication/password-reset/${req.params.token}`, req.body)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    })
});

module.exports = router;
