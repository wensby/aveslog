var express = require('express');
var router = express.Router();
const axios = require('axios');

router.post('/:id/common-names', function (req, res) {
  axios.post(`/birds/${req.params.id}/common-names`,
    req.body,
    {
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
