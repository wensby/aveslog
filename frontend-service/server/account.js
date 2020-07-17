var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/roles', (req, res) => {
  axios.get('/account/roles', {
    headers: {
      accessToken: req.header('accessToken'),
    },
  })
    .then(response => res.json(response.data))
    .catch(error => console.log(error));
});

module.exports = router;
