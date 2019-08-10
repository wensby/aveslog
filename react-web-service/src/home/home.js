import React from 'react';
import { useTranslation } from 'react-i18next';

export default function Home(props) {
  const { t } = useTranslation();

  if (props.authenticated) {
    return (
      <h1>{t("It's birding time!")}</h1>
    );
  }

  return (null);
}
