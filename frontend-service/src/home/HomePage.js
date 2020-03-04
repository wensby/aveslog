import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { FeedContainer } from './FeedContainer';
import { PageHeading } from '../generic/PageHeading.js';
import './HomePage.scss';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export const HomePage = () => {
  const { authenticated } = useContext(AuthenticationContext);
  const { t } = useTranslation();

  return (
    <div className='home-page'>
      <PageHeading>{t("It's birding time!")}</PageHeading>
      {authenticated && <FeedContainer />}
    </div>
  );
}
