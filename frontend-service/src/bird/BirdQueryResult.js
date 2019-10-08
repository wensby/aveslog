import React, { useState, useEffect, useContext } from 'react';
import { Link } from "react-router-dom";
import queryString from 'query-string';
import BirdService from './BirdService.js';
import { useTranslation } from 'react-i18next';
import './style.css';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import Loading from '../loading/Loading';

export default function BirdQueryResult(props) {
  const { t } = useTranslation();
  const query = queryString.parse(props.location.search).q;
  const [resultItems, setResultItems] = useState([]);
  const [displayedQuery, setDisplayedQuery] = useState(null);
  const [loading, setLoading] = useState(false);
  const { authenticated } = useContext(AuthenticationContext);

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

  const renderItemPicture = item => {
    if (item.thumbnail) {
      return (
        <img style={{ maxHeight: '150px' }}
          src={item.thumbnail} alt="Card" />
        );
    }
    return (
      <img style={{ maxHeight: '150px' }}
        src='/placeholder-bird.jpg' alt="Card cap" />
      );
  };

  const renderItemName = item => {
    const localeName = t(`bird:${item.binomialName}`, {fallbackLng: []});
    if (localeName !== item.binomialName) {
      return [
        <h5 key='1' className="card-title">{localeName}</h5>,
        <h6 key='2' className="card-subtitle mb-2 text-muted">
          {item.binomialName}
        </h6>
      ];
    }
    else {
      return <h5 key='1' className="card-title">{item.binomialName}</h5>;
    }
  };

  const renderAddSightingLink = item => {
    if (authenticated) {
      const formattedName = item.binomialName.toLowerCase().replace(' ', '-');
      const path = `/bird/${formattedName}/new-sighting`;
      return <Link to={path}>{t('add-sighting-link')}</Link>;
    }
    else {
      return null;
    }
  };

  const renderItem = (item, index) => {
    const formattedName = item.binomialName.toLowerCase().replace(' ', '-');
    return (<div key={index} className="card">
      <div className="card-horizontal">
        <div className="img-square-wrapper">
          <Link to={`/bird/${formattedName}`}>
            {renderItemPicture(item)}
          </Link>
        </div>
        <div className="card-body">
          {renderItemName(item)}
          {renderAddSightingLink(item)}
        </div>
      </div>
    </div>);
  };
  
  const renderItems = () => {
    return resultItems.map(renderItem);
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
