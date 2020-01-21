import React, { useState } from 'react';
import SightingSuccess from './SightingSuccess';
import './style.scss';
import { NewSightingForm } from './NewSightingForm';
import { useBird } from '../bird/BirdHooks';

export function NewBirdSighting({ match }) {
  const binomialName = match.params.birdId;
  const bird = useBird(binomialName);
  const [addedSighting, setAddedSighting] = useState(null);

  if (!bird) {
    return null;
  }

  if (addedSighting) {
    return <SightingSuccess sighting={addedSighting}/>;
  }

  return <NewSightingForm bird={bird} onSuccess={setAddedSighting}/>;
}
