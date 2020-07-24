import React from 'react';
import { BirderPage } from 'pages';
import { useBirderPage } from './BirderHooks';
import { LoadingOverlay } from 'loading/LoadingOverlay';

export function BirderPageContainer({ birderId }) {
  const { data, loading } = useBirderPage(birderId);
  if (loading) {
    return <div><LoadingOverlay /></div>;
  }
  return <BirderPage data={data} />;
}
