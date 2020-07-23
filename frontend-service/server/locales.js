var express = require('express');
var router = express.Router();

router.get('/', function (req, res) {
  req.axios.get('/locales').then(response => res.json(response.data));
});

module.exports = router;
