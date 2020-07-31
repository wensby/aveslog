import React, { useContext, useState, useEffect } from 'react';
import Spinner from 'loading/Spinner';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { BirdersList } from 'home/BirdersList';
import { PageHeading } from 'generic/PageHeading';
import { useTranslation } from 'react-i18next';
import './BirdersPage.scss';
import axios from 'axios';

export default () => {
  const { authenticated } = useContext(AuthenticationContext);
  const [loading, setLoading] = useState(true);
  const [birders, setBirders] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const fetchAccounts = async () => {
      const response = await axios.get('/api/birders')
      if (response.status === 200) {
        setBirders(response.data.items);
        setLoading(false);
      }
    }
    fetchAccounts();
  }, [authenticated]);

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
