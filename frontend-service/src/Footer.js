import React from 'react';
import { useTranslation } from 'react-i18next';
import './footer.scss';

const LanguageLink = ({ languageCode, label }) => {
  const { i18n } = useTranslation();

  const changeLanguage = lng => {
    i18n.changeLanguage(lng);
  };

  const handleClick = () => changeLanguage(languageCode);

  if (i18n.language === languageCode) {
    return <p className='selected'>{label}</p>;
  }
  return <button className='language-option' onClick={handleClick}>{label}</button>;
}

export default () => {
  return (
    <footer className='text-muted'>
      <div className='language'>
        <LanguageLink languageCode='en' label='English' />
        <LanguageLink languageCode='sv' label='Svenska' />
        <LanguageLink languageCode='ko' label='한국어' />
      </div>
    </footer>
  );
}
