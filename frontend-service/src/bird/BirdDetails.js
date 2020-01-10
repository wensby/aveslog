import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from '../sighting/NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';
import { useBird } from './BirdHooks';

export default function BirdDetails(props) {
  const { t, i18n } = useTranslation();
  const { authenticated } = useContext(UserContext);
  const bird = useBird(props.match.params.binomialName);

  const renderCoverNameCard = () => {
    const language = i18n.languages[0];
    const localeName = bird.names && bird.names[language] ? bird.names[i18n.languages[0]] : '';
    return (
      <div className='w-100 d-flex justify-content-center'>
        <div className='shadow bg-white text-center pt-1 mb-0 px-2 rounded-top'>
          <h1 className='text-dark bird-page-name pb-2 mb-0'>
            { localeName }</h1>
          <p className='font-italic font-weight-light text-muted mb-0 pb-2'>
            { bird.binomialName }</p>
        </div>
      </div>
    );
  }

  const renderCover = () => {
    let style = {};
    if (bird.cover) {
      style = { backgroundImage: `url(${bird.cover.url})` };
    }
    else {
      style = {};
    }
    return (
      <div className='picture-cover-container rounded-top overflow-hidden'
        style={style}>
        <div className='picture-cover'></div>
        {renderCoverNameCard()}
      </div>
    );
  }

  const renderPhotoCredits = () => {
    if (bird.thumbnail) {
      return (
        <div>
          <p><small>{`Thumbnail Photo by: ${ bird.thumbnail.credit }`}</small></p>
        </div>
      );
    }
  }

  const renderAddSighting = () => {
    if (authenticated) {
      return <NewBirdSightingLink bird={bird}>{t('add-sighting-link')}</NewBirdSightingLink>;
    }
  }

  if (bird) {
    return (
      <div>
        {renderCover()}
        {renderPhotoCredits()}
        {renderAddSighting()}
      </div>
    );
  }
  else {
    return null;
  }
}
