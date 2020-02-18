import { useContext } from 'react';
import { UserContext } from './authentication/UserContext.js';
import { useTranslation } from 'react-i18next';

export const useMenuItems = () => {
  const { authenticated, account, unauthenticate } = useContext(UserContext);
  const { t } = useTranslation();

  if (authenticated && account) {
    return [
      { label: t('Profile'), link: `/profile/${account.username}` },
      { label: t('Sightings'), link: '/sighting' },
      { label: t('birders'), link: '/profile', },
      { label: t('Settings'), link: '/settings' },
      { label: t('Logout'), action: unauthenticate }
    ];
  } else {
    return [
      { label: t('Login'), link: '/authentication/login' }
    ];
  }
};
