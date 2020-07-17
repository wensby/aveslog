import React from 'react';
import './DateDelimiter.scss';
import { useTranslation } from 'react-i18next';

export function DateDelimiter({ date }) {
  const { t } = useTranslation();
  const today = withoutTime(new Date(date)) === withoutTime(new Date());
  return <div className='date-delimiter'>{today ? t('today') : date}</div>;
}

function withoutTime(date) {
  return date.setHours(0,0,0,0);
}
