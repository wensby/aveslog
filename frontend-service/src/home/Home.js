import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { Link } from 'react-router-dom';
import AccountService from '../account/AccountService';

export default () => {
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);
  const { t } = useTranslation();
  const [usernames, setUsernames] = useState([]);
  const accountService = new AccountService();

  const fetchAccounts = async () => {
    const accessToken = await getAccessToken();
    const accounts = await accountService.fetchAccounts(accessToken);
    setUsernames(accounts.map(a => a.username));
  }

  useEffect(() => {
    if (authenticated) {
      fetchAccounts();
    }
  }, []);

  if (authenticated) {
    return (
      <>
        <h1>{t("It's birding time!")}</h1>
        {usernames.map(name => (
          <div>
            <Link to={`/profile/${name}`}>{name}</Link>
          </div>
        ))}
      </>
    );
  }

  return (null);
}
