var express = require('express');
var router = express.Router();

router.get('/:id', (req, res) => {
  const birderPromise = req.axios.get(`/birders/${req.params.id}`)
  .then(response => response.data);
  const sightingsPromise = req.axios.get(`/birders/${req.params.id}/sightings`)
  .then(response => response.data);
  Promise.all([birderPromise, sightingsPromise])
    .then(([birder, sightings]) => {
      res.json({ birder, sightings });
    });
});

module.exports = router;
