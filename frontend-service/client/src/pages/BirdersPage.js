import React, { useContext, useState, useEffect } from 'react';
import Spinner from 'loading/Spinner';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { BirdersList } from 'home/BirdersList';
import { ApiContext } from 'api/ApiContext';
import { PageHeading } from 'generic/PageHeading';
import { useTranslation } from 'react-i18next';
import './BirdersPage.scss';

export default () => {
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);
  const { authenticatedApiFetch } = useContext(ApiContext);
  const [loading, setLoading] = useState(true);
  const [birders, setBirders] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const fetchAccounts = async () => {
      const response = await authenticatedApiFetch('/api/birders', {})
      if (response.status === 200) {
        const json = await response.json();
        setBirders(json.items);
        setLoading(false);
      }
    }
    fetchAccounts();
  }, [authenticated, getAccessToken, authenticatedApiFetch]);

  if (loading) {
    return <Spinner />;
  }

  return (
    <div className='birders-page'>
      <PageHeading>{t('birders')}</PageHeading>
      <BirdersList birders={birders} />
    </div>
  );
};
