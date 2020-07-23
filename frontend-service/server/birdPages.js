var express = require('express');
var router = express.Router();

router.get('/:id', (req, res) => {
  const commonNamesPromise = req.axios.get(`/birds/${req.params.id}/common-names`)
    .then(response => response.data.items);
  const birdPromise = req.axios.get(`/birds/${req.params.id}`)
    .then(response => response.data);
  const statisticsPromise = req.axios.get(`/birds/${req.params.id}/statistics`)
    .then(response => response.data);
  Promise.all([commonNamesPromise, birdPromise, statisticsPromise])
    .then(([commonNames, bird, statistics]) => {
      res.json({ bird, commonNames, statistics });
    });
});

module.exports = router;
