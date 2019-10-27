import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext';

export default () => {
  const { authenticated } = useContext(UserContext);
  const { t } = useTranslation();

  if (!authenticated) {
    return null;
  }
  return (
    <>
      <h1>{t("It's birding time!")}</h1>
    </>
  );
}
