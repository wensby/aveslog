import React from 'react';
import queryString from 'query-string';

import { BirdSearchResultsContainer } from './BirdSearchResultsContainer.js';

export function BirdSearchResultsPage({ location }) {
  const query = queryString.parse(location.search).q;
  return <BirdSearchResultsContainer query={query} />
}
