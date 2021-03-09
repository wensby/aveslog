import React, { useContext } from 'react';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { useTranslation } from 'react-i18next';
import { PageHeading } from '../generic/PageHeading.js';
import { FeedContainer } from '../home/FeedContainer';
import './HomePage.scss';

export default () => {
  const { authenticated } = useContext(AuthenticationContext);
  const { t } = useTranslation();

  return (
    <div className='home-page'>
      <PageHeading>{t("It's birding time!")}</PageHeading>
      {authenticated && <FeedContainer />}
    </div>
  );
}
