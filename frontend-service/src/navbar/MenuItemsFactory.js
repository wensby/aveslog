import React from 'react';
import { Link } from 'react-router-dom';

const getMenuItems = (authenticated, account, unauthenticate, t) => {
  if (authenticated && account) {
    return [
      <Link className="nav-link"
          to={`/profile/${account.username}`}>{t('Profile')}</Link>,
      <Link className="nav-link"
          to={'/sighting'}>{t('Sightings')}</Link>,
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
}

export { getMenuItems };
