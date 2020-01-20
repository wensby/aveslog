import React, { useContext, useState, useEffect } from 'react';
import Spinner from '../loading/Spinner';
import { UserContext } from '../authentication/UserContext';
import AccountService from '../account/AccountService';
import AccountLink from './AccountLink';

export function Accounts() {
  const { authenticated, getAccessToken } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const [usernames, setUsernames] = useState([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      const accessToken = await getAccessToken();
      const response = await new AccountService().fetchAccounts(accessToken);
      if (response.status === 200) {
        const json = await response.json();
        setUsernames(json.items.map(a => a.username));
        setLoading(false);
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

  return usernames.map(name => (<AccountLink key={name} name={name}/>));
}
