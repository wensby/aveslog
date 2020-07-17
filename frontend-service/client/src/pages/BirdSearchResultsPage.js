import React from 'react';
import queryString from 'query-string';

import { BirdSearchResultsContainer } from '../bird/BirdSearchResultsContainer.js';

export default ({ location }) => {
  const query = queryString.parse(location.search).q;
  return <BirdSearchResultsContainer query={query} />
};
