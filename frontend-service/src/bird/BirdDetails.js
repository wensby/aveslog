import React, { useState, useEffect, useContext } from 'react';
import BirdService from './BirdService';
import { useTranslation } from 'react-i18next';
import NewBirdSightingLink from './NewBirdSightingLink';
import { UserContext } from '../authentication/UserContext';

export default function BirdDetails(props) {
  const { t } = useTranslation();
  const { authenticated } = useContext(UserContext);
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const service = new BirdService();
      const data = await service.getBird(props.match.params.binomialName);
      setData(data);
    }
    fetchData();
  }, [props.match.params.binomialName]);

  const renderCoverNameCard = () => {
    return (
      <div className='w-100 d-flex justify-content-center'>
        <div className='shadow bg-white text-center pt-1 mb-0 px-2 rounded-top'>
          <h1 className='text-dark bird-page-name pb-2 mb-0'>
            { t(`bird:${data.binomialName}`) }</h1>
          <p className='font-italic font-weight-light text-muted mb-0 pb-2'>
            { data.binomialName }</p>
        </div>
      </div>
    );
  }

  const renderCover = () => {
    let style = {};
    if (data.cover) {
      style = { backgroundImage: `url(${data.cover.url})` };
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
    if (data.thumbnail) {
      return (
        <div>
          <p><small>{`Thumbnail Photo by: ${ data.thumbnail.credit }`}</small></p>
        </div>
      );
    }
  }

  const renderAddSighting = () => {
    if (authenticated) {
      return <NewBirdSightingLink bird={data}>{t('add-sighting-link')}</NewBirdSightingLink>;
    }
  }

  if (data) {
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
