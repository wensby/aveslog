import React from 'react';
import { BirderPage } from 'pages';
import Spinner from '../loading/Spinner';
import { useBirder } from './BirderHooks';

export function BirderPageContainer({ birderId }) {
  const { birder, loading } = useBirder(birderId);
  if (loading) {
    return <div><Spinner /></div>;
  }
  return <BirderPage birder={birder} />;
}
