import React, { useContext, useState, useEffect } from 'react';
import { Feed } from './Feed';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { HomeContext } from 'specific/HomeContext';

const FeedContext = React.createContext();

export const FeedContainer = () => {
  const { getAccessToken, authenticated } = useContext(AuthenticationContext);
  const { homeTrigger } = useContext(HomeContext);
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchItems = async () => {
      const accessToken = await getAccessToken();
      if (accessToken) {
        const response = await fetch('/api/home-feed', {
          headers: {
            'accessToken': accessToken.jwt,
          },
        });
        if (response.status === 200) {
          const json = await response.json();
          setItems(json.items);
        }
      }
    }
    if (authenticated) {
      fetchItems();
    }
  }, [authenticated, getAccessToken, homeTrigger]);

  return (
    <FeedContext.Provider value={{ items }}>
      <Feed items={items} />
    </FeedContext.Provider>
  );
}
