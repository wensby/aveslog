import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext';
import { FeedContainer } from './FeedContainer';
import { PageHeading } from '../generic/PageHeading.js';
import './HomePage.scss';

export const HomePage = () => {
  const { authenticated } = useContext(UserContext);
  const { t } = useTranslation();

  return (
    <div className='home-page'>
      <PageHeading>{t("It's birding time!")}</PageHeading>
      {authenticated && <FeedContainer />}
    </div>
  );
}
