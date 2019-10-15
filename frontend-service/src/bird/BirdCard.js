import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from "react-router-dom";
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import BirdCardPicture from './BirdCardPicture';
import NewBirdSightingLink from './NewBirdSightingLink';

export default ({bird, key}) => {
  const { t } = useTranslation();
  const { authenticated } = useContext(AuthenticationContext);

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
      return <NewBirdSightingLink bird={item}>{t('add-sighting-link')}</NewBirdSightingLink>;
    }
    else {
      return null;
    }
  };


  const formattedName = bird.binomialName.toLowerCase().replace(' ', '-');

  return (<div key={key} className="card">
    <div className="card-horizontal">
      <div className="img-square-wrapper">
        <Link to={`/bird/${formattedName}`}>
          <BirdCardPicture bird={bird} />
        </Link>
      </div>
      <div className="card-body">
        {renderItemName(bird)}
        {renderAddSightingLink(bird)}
      </div>
    </div>
  </div>);
};
