import React from 'react';
import { BirderPage } from 'pages';
import Spinner from '../loading/Spinner';
import { useBirderPage } from './BirderHooks';

export function BirderPageContainer({ birderId }) {
  const { data, loading } = useBirderPage(birderId);
  if (loading) {
    return <div><Spinner /></div>;
  }
  return <BirderPage data={data} />;
}
