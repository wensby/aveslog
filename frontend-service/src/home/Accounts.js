import React, { useContext, useState, useEffect } from 'react';
import Spinner from '../loading/Spinner';
import AccountService from '../account/AccountService';
import { BirderLink } from './BirderLink';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export const Accounts = () => {
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);
  const [loading, setLoading] = useState(true);
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      const accessToken = await getAccessToken();
      if (accessToken) {
        const response = await new AccountService().fetchAccounts(accessToken);
        if (response.status === 200) {
          const json = await response.json();
          setAccounts(json.items);
          setLoading(false);
        }
      }
    }
    if (authenticated) {
      fetchAccounts();
    }
    else {
      setLoading(false);
    }
  }, [authenticated, getAccessToken]);

  if (loading) {
    return <Spinner />;
  }

  return accounts.map(account => (<BirderLink key={account.username} birder={account.birder} />));
};
