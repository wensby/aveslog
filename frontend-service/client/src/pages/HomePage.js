import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { AuthenticationContext } from 'authentication/AuthenticationContext';
import { PageHeading } from 'generic/PageHeading';
import { FeedContainer } from 'home/FeedContainer';
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
