import React from 'react';
import { useTranslation } from "react-i18next";
export function Label({ htmlFor, label }) {
  const { t } = useTranslation();
  return <label htmlFor={htmlFor}>{t(label)}</label>;
}
