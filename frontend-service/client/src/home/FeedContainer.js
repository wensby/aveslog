import React, { useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { Feed } from './Feed';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { HomeContext } from 'specific/HomeContext';
import { LoadingOverlay } from 'loading/LoadingOverlay';

const FeedContext = React.createContext();

export const FeedContainer = () => {
  const { authenticated } = useContext(AuthenticationContext);
  const { homeTrigger } = useContext(HomeContext);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    axios.get('/api/home-feed')
      .then(response => {
        setItems(response.data.items)
        setLoading(false)
      })
  }, [authenticated, homeTrigger]);

  return (
    <FeedContext.Provider value={{ items }}>
      {loading && <LoadingOverlay />}
      {!loading && <Feed items={items} />}
    </FeedContext.Provider>
  );
}
