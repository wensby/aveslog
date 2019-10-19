import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext';
import { Link } from 'react-router-dom';
import AccountService from '../account/AccountService';
import Spinner from '../loading/Spinner';

export default () => {
  const { authenticated, getAccessToken } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const { t } = useTranslation();
  const [usernames, setUsernames] = useState([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      const accessToken = await getAccessToken();
      const accounts = await new AccountService().fetchAccounts(accessToken);
      setUsernames(accounts.map(a => a.username));
      setLoading(false);
    }
    if (authenticated) {
      fetchAccounts();
    }
    else {
      setLoading(false);
    }
  }, [authenticated, getAccessToken]);

  if (loading) {
    return <Spinner/>;
  }
  return (
    <>
      <h1>{t("It's birding time!")}</h1>
      {usernames.map(name => (
        <div key={name}>
          <Link to={`/profile/${name}`}>{name}</Link>
        </div>
      ))}
    </>
  );
}
