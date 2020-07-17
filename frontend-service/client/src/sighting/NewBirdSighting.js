import React, { useState } from 'react';
import { SightingSuccess } from './SightingSuccess';
import { LogBirdSection } from './LogBirdSection';
import { useBird } from '../bird/BirdHooks';

export const NewBirdSighting = ({ match }) => {
  const binomialName = match.params.birdId;
  const { bird } = useBird(binomialName);
  const [addedSighting, setAddedSighting] = useState(null);

  if (!bird) {
    return null;
  }

  if (addedSighting) {
    return <SightingSuccess sighting={addedSighting}/>;
  }

  return <LogBirdSection bird={bird} onSuccess={setAddedSighting}/>;
};
