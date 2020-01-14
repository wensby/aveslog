import React, { useState, useEffect } from 'react';
import queryString from 'query-string';
import BirdService from './BirdService.js';
import './style.scss';
import Loading from '../loading/Loading';
import BirdResultCard from './BirdResultCard';
import { useTranslation } from 'react-i18next';

export function BirdSearchResultsPage({ location }) {
  const query = queryString.parse(location.search).q;
  const [resultItems, setResultItems] = useState([]);
  const [displayedQuery, setDisplayedQuery] = useState(null);
  const [loading, setLoading] = useState(false);
  const { t } = useTranslation();

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

  const renderLoading = () => {
    if (loading) {
      return <Loading />;
    }
    return null;
  };

  return (
    <div className='bird-result-container text-break'>
      <div className='info'>{t('result-info-label')}: {query}</div>
      {resultItems.map((item, index) => <BirdSearchResultItem
        item={item}
        key={index}
      />)}
      {renderLoading()}
    </div>
  );
}

function BirdSearchResultItem({ item, ...props }) {
  return (
    <React.Fragment {...props}>
      <BirdResultCard searchResult={item} />
    </React.Fragment>
  );
}
