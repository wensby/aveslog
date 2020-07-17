var express = require('express');
var router = express.Router();
const axios = require('axios');

router.post('/password-reset', (req, res) => {
  axios.post('/authentication/password-reset', req.body)
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
  axios.post(`/authentication/password-reset/${req.params.token}`, req.body)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    })
});

module.exports = router;
