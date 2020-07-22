var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/:id', (req, res) => {
  const commonNamesPromise = axios.get(`/birds/${req.params.id}/common-names`)
    .then(response => response.data.items);
  const birdPromise = axios.get(`/birds/${req.params.id}`)
    .then(response => response.data);
  const statisticsPromise = axios.get(`/birds/${req.params.id}/statistics`)
    .then(response => response.data);
  Promise.all([commonNamesPromise, birdPromise, statisticsPromise])
    .then(([commonNames, bird, statistics]) => {
      res.json({ bird, commonNames, statistics });
    });
});

module.exports = router;
