import React from 'react';
import { BirdResultCard } from './BirdResultCard';
import { useTranslation } from 'react-i18next';
import './BirdSearchResults.scss';

export const BirdSearchResults = ({ query, birds }) => {
  const { t } = useTranslation();

  return (
    <div className='bird-result-container'>
      <div className='info'>{t('result-info-label')}: {query}</div>
      {birds.map((item, index) => <BirdSearchResultItem
        item={item}
        key={index}
      />)}
    </div>
  );
};

const BirdSearchResultItem = ({ item }) => {
  return <BirdResultCard searchResult={item} />;
};
