import React from 'react';
import { BirdResultCard, BirdResultCardPlaceholder } from './BirdResultCard';
import { useTranslation } from 'react-i18next';
import './style.scss';
import { LazyLoad } from '../LazyLoad.js';

export function BirdSearchResults({ query, birds }) {
  const { t } = useTranslation();

  return (
    <div className='bird-result-container text-break'>
      <div className='info'>{t('result-info-label')}: {query}</div>
      {birds.map((item, index) => <BirdSearchResultItem
        item={item}
        key={index}
      />)}
    </div>
  );
};

function BirdSearchResultItem({ item, key }) {
  return (
    <LazyLoad offset={300} key={key} placeholder={<BirdResultCardPlaceholder />}>
      <BirdResultCard searchResult={item} />
    </LazyLoad>
  );
}
