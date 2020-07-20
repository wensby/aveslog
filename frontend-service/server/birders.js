var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/:id/birder-connections', (req, res) => {
  axios.get(`/birders/${req.params.id}/birder-connections`, {
    headers: {
      accessToken: req.header('accessToken'),
    },
  })
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

router.post('/:id/birder-connections', (req, res) => {
  axios.post(`/birders/${req.params.id}/birder-connections`, req.body, {
    headers: {
      accessToken: req.header('accessToken'),
    },
  })
    .then(response => {
      res.set('location', response.headers['location']);
      res.status(response.status);
      res.json(response.data);
    });
});

module.exports = router;
