import React from 'react';
import { useTranslation } from 'react-i18next';
import './Footer.scss';

export const Footer = () => {
  return (
    <footer>
      <div className='languages'>
        <LanguageLink languageCode='en' label='English' />
        <LanguageLink languageCode='sv' label='Svenska' />
        <LanguageLink languageCode='ko' label='한국어' />
      </div>
    </footer>
  );
};

const LanguageLink = ({ languageCode, label }) => {
  const { i18n } = useTranslation();

  const handleClick = () => {
    i18n.changeLanguage(languageCode);
  };

  if (i18n.languages[0] === languageCode) {
    return <p className='selected'>{label}</p>;
  }
  return <button onClick={handleClick}>{label}</button>;
}
