import React, { useContext } from 'react';
import { UserContext } from './authentication/UserContext.js';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

export const useMenuItems = () => {
  const { authenticated, account, unauthenticate } = useContext(UserContext);
  const { t } = useTranslation();

  if (authenticated && account) {
    return [
      <Link className="nav-link"
          to={`/profile/${account.username}`}>{t('Profile')}</Link>,
      <Link className="nav-link"
          to={'/sighting'}>{t('Sightings')}</Link>,
      <Link className='nav-link' to={'/profile'}>{t('birders')}</Link>,
      <Link className="nav-link"
          to={'/settings'}>{t('Settings')}</Link>,
      <Link className="nav-link" onClick={unauthenticate}
          to={'/authentication/logout'}>{t('Logout')}</Link>
    ];
  } else {
    return [
      <Link className="nav-link"
          to={'/authentication/login'}>{t('Login')}</Link>,
    ];
  }
};
