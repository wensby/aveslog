import React, { useState, useEffect } from 'react';
import queryString from 'query-string';
import BirdService from './BirdService.js';
import './style.css';
import Loading from '../loading/Loading';
import BirdResultCard from './BirdResultCard';

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
          if (response.status === 200) {
          setResultItems((await response.json()).items);
        }
        setDisplayedQuery(query);
        setLoading(false);
      }
    }
    fetchResult();
  }, [query, displayedQuery]);

  const renderItems = () => {
    return resultItems.map((item, index) => {
      return (
        <React.Fragment key={index}>
          <BirdResultCard searchResult={item} />
        </React.Fragment>
      );
    });
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
