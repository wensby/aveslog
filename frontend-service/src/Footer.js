import React from 'react';
import { useTranslation } from 'react-i18next';
import './footer.css';

const LanguageLink = ({ languageCode, label }) => {
  const { i18n } = useTranslation();

  const changeLanguage = lng => {
    i18n.changeLanguage(lng);
  };

  const handleClick = () => changeLanguage(languageCode);

  return <a href='javascipt:void(0)' onClick={handleClick}>{label}</a>;
}

export default () => {
  return (
    <footer className='text-muted'>
      <div className='language'>
        <LanguageLink languageCode='en' label='English' />
        <LanguageLink languageCode='sv' label='Svenska' />
        <LanguageLink languageCode='kr' label='한국어' />
      </div>
    </footer>
  );
}
