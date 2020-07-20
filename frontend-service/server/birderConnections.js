var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/:id', (req, res) => {
  axios.get(`/birder-connections/${req.params.id}`, {
    headers: {
      accessToken: req.header('accessToken'),
    },
  })
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

router.delete('/:id', (req, res) => {
  axios.delete(`/birder-connections/${req.params.id}`, {
    headers: {
      accessToken: req.header('accessToken'),
    },
  })
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

module.exports = router;
