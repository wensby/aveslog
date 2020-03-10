import { useContext } from 'react';
import { AuthenticationContext } from './authentication/AuthenticationContext.js';
import { UserContext } from './authentication/UserContext.js';
import { useTranslation } from 'react-i18next';

export const useMenuItems = () => {
  const { authenticated, unauthenticate } = useContext(AuthenticationContext);
  const { account } = useContext(UserContext);
  const { t } = useTranslation();

  if (authenticated && account) {
    return [
      { label: t('Profile'), link: `/birders/${account.birder.id}` },
      { label: t('Sightings'), link: '/sighting' },
      { label: t('birders'), link: '/birders', },
      { label: t('Settings'), link: '/settings' },
      { label: t('Logout'), action: unauthenticate }
    ];
  } else {
    return [
      { label: t('Login'), link: '/authentication/login' }
    ];
  }
};
