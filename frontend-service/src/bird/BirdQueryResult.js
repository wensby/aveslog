import React, { useState, useEffect } from 'react';
import queryString from 'query-string';
import BirdService from './BirdService.js';
import './style.css';
import Loading from '../loading/Loading';
import BirdCard from './BirdCard';

export default function BirdQueryResult(props) {
  const query = queryString.parse(props.location.search).q;
  const [resultItems, setResultItems] = useState([]);
  const [displayedQuery, setDisplayedQuery] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchResult = async () => {
      if (query !== displayedQuery) {
        setLoading(true);
        const service = new BirdService();
        const response = await service.queryBirds(query);
        if (response.status === 'success') {
          setResultItems(response.result);
        }
        setDisplayedQuery(query);
        setLoading(false);
      }
    }
    fetchResult();
  }, [query, displayedQuery]);

  const renderItems = () => {
    return resultItems.map((item, index) => <BirdCard bird={item} key={index} />);
  };

  const renderLoading = () => {
    if (loading) {
      return <Loading />;
    }
    return null;
  };

  return (
    <div className='bird-result-container text-break'>
      {renderItems()}
      {renderLoading()}
    </div>
  );
}
