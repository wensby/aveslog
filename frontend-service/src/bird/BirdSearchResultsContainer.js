import React, { useState, useEffect } from 'react';
import BirdService from './BirdService.js';
import './style.scss';
import Loading from '../loading/Loading';
import { BirdSearchResults } from './BirdSearchResults.js';

export function BirdSearchResultsContainer({ query }) {
  const [resultItems, setResultItems] = useState([]);
  const [displayedQuery, setDisplayedQuery] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchResult = async () => {
      if (query !== displayedQuery) {
        setLoading(true);
        const service = new BirdService();
        const response = await service.searchBirds(query);
        if (response.status === 200) {
          setResultItems((await response.json()).items);
        }
        setDisplayedQuery(query);
        setLoading(false);
      }
    }
    fetchResult();
  }, [query, displayedQuery]);

  if (loading) {
    return <div className='bird-result-container text-break'><Loading /></div>;
  }
  return <BirdSearchResults query={query} birds={resultItems} />;
};