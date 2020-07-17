var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/', function (req, res) {
  axios.get('/locales').then(response => res.json(response.data));
});

module.exports = router;
