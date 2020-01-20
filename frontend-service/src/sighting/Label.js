import React from 'react';
import { useTranslation } from "react-i18next";
export function Label({ htmlFor, label }) {
  const { t } = useTranslation();
  const className = 'col-sm-2 col-form-label';
  return <label htmlFor={htmlFor} className={className}>{t(label)}</label>;
}
