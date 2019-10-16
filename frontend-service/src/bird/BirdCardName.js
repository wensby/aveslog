import React from 'react';
import { useTranslation } from 'react-i18next';

export default ({ bird }) => {
  const { t } = useTranslation();
  const localeName = t(`bird:${bird.binomialName}`, { fallbackLng: [] });
  if (localeName === bird.binomialName) {
    return <h5 key='1' className="card-title">{bird.binomialName}</h5>;
  }
  return (
    <>
      <h5 key='1' className="card-title">{localeName}</h5>
      <h6 key='2' className="card-subtitle mb-2 text-muted">
        {bird.binomialName}
      </h6>
    </>
  );
};
