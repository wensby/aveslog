import React, { useContext, useState, useEffect } from 'react';
import Spinner from 'loading/Spinner';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { Accounts } from 'home/Accounts';
import { ApiContext } from 'api/ApiContext';

export default () => {
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);
  const { authenticatedApiFetch } = useContext(ApiContext);
  const [loading, setLoading] = useState(true);
  const [birders, setBirders] = useState([]);

  useEffect(() => {
    const fetchAccounts = async () => {
      const response = await authenticatedApiFetch('/birders', {})
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
    <div>
      <Accounts birders={birders} />
    </div>
  );
};
