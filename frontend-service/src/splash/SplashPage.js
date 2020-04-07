import React, { useContext, useEffect } from 'react';
import { SearchContext } from 'search/SearchContext';
import { Brand } from 'specific/Brand';
import { SearchForm } from './SearchForm.js';
import { UserContext } from 'authentication/UserContext';
import { Link } from 'react-router-dom';
import {Footer} from 'footer/Footer.js';
import { useTranslation } from 'react-i18next';
import './SplashPage.scss';

export const SplashPage = () => {
  const { clear } = useContext(SearchContext);

  useEffect(() => {
    clear();
  }, []);

  return (
    <div className='splash-page'>
      <Link to ='/home'>
        <Brand />
      </Link>
      <LoginSection />
      <SearchForm />
      <Footer />
    </div>
  );
};

const LoginSection = () => {
  const { account } = useContext(UserContext);
  const { t } = useTranslation();
  return (
    <div className='login-section'>
      {account && <span>{t('birder-label')}: <Link to={`/birders/${account.birder.id}`}>{account.birder.name}</Link></span>}
      {!account && <Link to={`/authentication/login`}>{t('Login')}</Link>}
    </div>
  );
}
