import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext';
import { FeedContainer } from './FeedContainer';

export const HomePage = () => {
  const { authenticated } = useContext(UserContext);
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t("It's birding time!")}</h1>
      {authenticated && <FeedContainer />}
    </div>
  );
}
