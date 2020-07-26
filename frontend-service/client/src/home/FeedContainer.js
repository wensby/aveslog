import React, { useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { Feed } from './Feed';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { HomeContext } from 'specific/HomeContext';

const FeedContext = React.createContext();

export const FeedContainer = () => {
  const { authenticated } = useContext(AuthenticationContext);
  const { homeTrigger } = useContext(HomeContext);
  const [items, setItems] = useState([]);

  useEffect(() => {
    axios.get('/api/home-feed')
      .then(response => setItems(response.data.items));
  }, [authenticated, homeTrigger]);

  return (
    <FeedContext.Provider value={{ items }}>
      <Feed items={items} />
    </FeedContext.Provider>
  );
}
