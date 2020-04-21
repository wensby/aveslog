import React, { useContext, useEffect } from 'react';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { useTranslation } from 'react-i18next';
import { PageHeading } from '../generic/PageHeading.js';
import { FeedContainer } from './FeedContainer';
import './HomePage.scss';
import { HomeContext } from 'specific/HomeContext';

export const HomePage = () => {
  const { authenticated } = useContext(AuthenticationContext);
  const { t } = useTranslation();
  const { homeTrigger } = useContext(HomeContext);

  return (
    <div className='home-page'>
      <PageHeading>{t("It's birding time!")}</PageHeading>
      {authenticated && <FeedContainer />}
    </div>
  );
}
