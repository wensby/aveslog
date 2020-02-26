import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext';
import { SightingFeedContainer } from './SightingFeedContainer';

export const HomePage = () => {
  const { authenticated } = useContext(UserContext);
  const { t } = useTranslation();

  if (!authenticated) {
    return null;
  }
  return (
    <div>
      <h1>{t("It's birding time!")}</h1>
      <SightingFeedContainer />
    </div>
  );
}
