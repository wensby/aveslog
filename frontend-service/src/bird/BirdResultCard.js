import React, { useState, useEffect } from 'react';
import BirdCard from './BirdCard';
import birdRepository from './BirdRepository';

export default ({ searchResult, ...other }) => {
  const [bird, setBird] = useState(null);

  const resultBird = async birdId => {
    setBird(await birdRepository.getBird(birdId));
  }

  useEffect(() => {
    resultBird(searchResult.birdId);
  }, [searchResult]);

  if (bird) {
    return <BirdCard bird={bird} {...other} />
  }
  else {
    return null;
  }
}
