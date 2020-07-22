import React from 'react';
import { CoverNameCard } from './CoverNameCard';
import { useTranslation } from 'react-i18next';
import './BirdCover.scss';

export function BirdCover({ bird, commonNames }) {
  const { i18n } = useTranslation();
  const language = i18n.languages[0];
  const commonName = commonNames.find(l => l.locale === language);
  let style = {};
  if (bird.cover) {
    style = { backgroundImage: `url(${bird.cover.url})` };
  }
  return (
    <div className='picture-cover-container' style={style}>
      <div className='picture-cover'></div>
      <CoverNameCard binomial={bird.binomialName} common={commonName.name} />
    </div>
  );
}
