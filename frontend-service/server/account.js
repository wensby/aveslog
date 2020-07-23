var express = require('express');
var router = express.Router();

router.get('/roles', (req, res) => {
  req.axios.get('/account/roles')
    .then(response => res.json(response.data))
    .catch(error => console.log(error));
});

module.exports = router;
