import React, { useContext, useState, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { FilterableSightingsList } from '../sighting/FilterableSightingsList';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';

export const BirderPage = ({ birder }) => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const { account } = useContext(UserContext);
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    const fetchSightings = async () => {
      const accessToken = await getAccessToken();
      if (accessToken) {
        const response = await new SightingService().fetchBirderSightings(birder.id, accessToken);
        if (response.status === 200) {
          const json = await response.json();
          setSightings(json.items);
        }
      }
    }
    fetchSightings();
  }, [birder, getAccessToken]);

  return (
    <div>
      <h1>{birder.name}</h1>
      <FilterableSightingsList sightings={sightings} />
    </div>
  );
};

const BirderConnectionButton = ({ birder }) => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const { account } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const [birderConnection, setBirderConnection] = useState(null);
  const { t } = useTranslation();
  const message = birderConnection == null ? 'birder-connection-following-label' : 'birder-connection-no-connection-label';

  useEffect(() => {
    const resolveFollows = async () => {
      setLoading(true);
      const accessToken = await getAccessToken();
      const response = await fetch(`${window._env_.API_URL}/birders/${account.birder.id}/birder-connections`, {
        headers: {
          'accessToken': accessToken.jwt
        }
      });
      if (response.status === 200) {
        const json = await response.json();
        const connection = json.items.find(bc => bc.secondaryBirderId === birder.id);
        if (connection) {
          setBirderConnection(connection);
        }
        else {
          setBirderConnection(null);
        }
        setLoading(false);
      }
    };
    resolveFollows();
  }, [birder]);

  const handleClick = e => {
    const updateBirderConnection = async () => {
      setLoading(true);
      if (birderConnection == null) {
        const accessToken = await getAccessToken();
        const response = await fetch(`${window._env_.API_URL}/birders/${account.birder.id}/birder-connections`, {
          method: 'POST',
          headers: {
            'accessToken': accessToken.jwt
          },
          body: JSON.stringify({ secondaryBirderId: birder.id })
        });
        if (response.status === 201) {
          const location = response.headers['Location'];
          const response = await fetch(`${window._env_.API_URL}${location}`, {
            headers: {
              accessToken: accessToken.jwt
            }
          });
          setBirderConnection(birderConnection == null);
          setLoading(false);
        }
      }
      else {

      }
    };
    updateBirderConnection();
  };

  return <button className='birder-connection-button' onClick={handleClick}>{loading ? '...' : t(message)}</button>;
};
