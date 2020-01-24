import React from 'react';
import { BirderPage } from './BirderPage';
import Spinner from '../loading/Spinner';
import { useBirder } from './BirderHooks';

export function BirderPageContainer({ birderId }) {
  const birder = useBirder(birderId);
  if (!birder) {
    return <div><Spinner /></div>;
  }
  return <BirderPage birder={birder} />;
}
