import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export default () => {
  const { authenticated } = useContext(AuthenticationContext);
  const { t } = useTranslation();

  if (authenticated) {
    return (
      <h1>{t("It's birding time!")}</h1>
    );
  }

  return (null);
}
