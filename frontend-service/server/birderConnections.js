var express = require('express');
var router = express.Router();

router.get('/:id', (req, res) => {
  req.axios.get(`/birder-connections/${req.params.id}`)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

router.delete('/:id', (req, res) => {
  req.axios.delete(`/birder-connections/${req.params.id}`)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

module.exports = router;
