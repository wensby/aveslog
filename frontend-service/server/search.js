var express = require('express');
var router = express.Router();

router.get('/', (req, res) => {
  req.axios.get('/search/birds', {
    params: {
      q: req.query.q,
      embed: 'stats',
    }
  })
    .then(response => response.data.items)
    .then(items => {
      const enrichedItemPromises = items.map(item => req.axios.get(`/birds/${item.id}?embed=commonNames`)
        .then(response => response.data)
        .then(bird => {
          return { bird: bird, ...item }
        }));
      return Promise.all(enrichedItemPromises);
    })
    .then(items => res.json({ items: items }));
});

module.exports = router;
