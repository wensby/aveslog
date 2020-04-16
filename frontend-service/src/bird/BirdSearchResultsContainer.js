import React, { useContext, useState, useEffect } from 'react';
import BirdService from './BirdService.js';
import { LoadingOverlay } from '../loading/LoadingOverlay';
import { BirdSearchResults } from './BirdSearchResults.js';
import { AuthenticationContext } from 'authentication/AuthenticationContext';

export const BirdSearchResultsContainer = ({ query }) => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [resultItems, setResultItems] = useState([]);
  const [displayedQuery, setDisplayedQuery] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchResult = async () => {
      if (query !== displayedQuery) {
        setLoading(true);
        const service = new BirdService();
        const accessToken = await getAccessToken();
        const response = await service.searchBirds(query, accessToken);
        if (response.status === 200) {
          setResultItems((await response.json()).items);
        }
        setDisplayedQuery(query);
        setLoading(false);
      }
    }
    fetchResult();
  }, [query, displayedQuery, getAccessToken]);

  if (loading) {
    return <LoadingOverlay />;
  }
  return <BirdSearchResults query={query} birds={resultItems} />;
};
