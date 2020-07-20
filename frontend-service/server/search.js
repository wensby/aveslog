var express = require('express');
var router = express.Router();
const axios = require('axios');

router.get('/', (req, res) => {
  const headers = {};
  if (req.header('accessToken')) {
    headers.accessToken = req.header('accessToken');
  }
  axios.get('/search/birds', {
    params: {
      q: req.query.q,
      embed: 'stats',
    },
    headers: headers,
  })
    .then(response => response.data.items)
    .then(items => {
      const enrichedItemPromises = items.map(item => axios.get(`/birds/${item.id}?embed=commonNames`)
        .then(response => response.data)
        .then(bird => {
          return { bird: bird, ...item }
        }));
      return Promise.all(enrichedItemPromises);
    })
    .then(items => res.json({ items: items }));
});

module.exports = router;
