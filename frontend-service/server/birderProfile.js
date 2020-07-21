var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/:id', (req, res) => {
  const accessToken = req.header('accessToken');
  const birderPromise = axios.get(`/birders/${req.params.id}`, {
    headers: {
      accessToken: accessToken
    }
  })
  .then(response => response.data);
  const sightingsPromise = axios.get(`/birders/${req.params.id}/sightings`, {
    headers: {
      accessToken: accessToken
    }
  })
  .then(response => response.data);
  Promise.all([birderPromise, sightingsPromise])
    .then(([birder, sightings]) => {
      res.json({ birder, sightings });
    });
});

module.exports = router;
