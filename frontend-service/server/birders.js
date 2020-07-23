var express = require('express');
var router = express.Router();

router.get('/:id/birder-connections', (req, res) => {
  req.axios.get(`/birders/${req.params.id}/birder-connections`)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

router.post('/:id/birder-connections', (req, res) => {
  req.axios.post(`/birders/${req.params.id}/birder-connections`, req.body)
    .then(response => {
      res.set('location', response.headers['location']);
      res.status(response.status);
      res.json(response.data);
    });
});

module.exports = router;
