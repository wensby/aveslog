const express = require('express');
const router = express.Router();

const unique = (value, index, self) => self.indexOf(value) === index;

router.get('/', async (req, res) => {
  try {
    const sightings = await req.axios.get('/sightings?limit=10')
      .then(response => response.data.items);
    const birdersPromise = Promise.all(sightings
      .map(s => s.birderId)
      .filter(unique)
      .map(id => req.axios.get(`/birders/${id}`)
        .then(response => response.data)));
    const birdsPromise = Promise.all(sightings
      .map(s => s.birdId)
      .filter(unique)
      .map(id => req.axios.get(`/birds/${id}?embed=commonNames`)
        .then(response => response.data)));
    const [birders, birds] = await Promise.all([birdersPromise, birdsPromise]);
    const enrichedSightings = sightings.map(s => {
      return {
        ...s,
        bird: birds.find(b => b.id === s.birdId),
        birder: birders.find(b => b.id === s.birderId),
      };
    })
    res.json({ items: enrichedSightings });
  } catch (error) {
    if (error.response) {
      res.status(error.response.status);
      res.json(error.response.data);
    }
  }
});

module.exports = router;
