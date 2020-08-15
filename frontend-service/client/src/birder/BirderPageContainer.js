import React from 'react';
import { BirderPage } from 'pages';
import { useBirderPage } from './BirderHooks';
import { LoadingOverlay } from 'loading/LoadingOverlay';

export function BirderPageContainer({ birderId }) {
  const { data, loading } = useBirderPage(birderId);
  return loading ? <LoadingOverlay /> : <BirderPage data={data} />;
}
