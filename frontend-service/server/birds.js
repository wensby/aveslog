var express = require('express');
var router = express.Router();

router.post('/:id/common-names', function (req, res) {
  req.axios.post(`/birds/${req.params.id}/common-names`, req.body)
    .then(response => {
      res.status(response.status);
      res.json(response.data);
    });
});

module.exports = router;
