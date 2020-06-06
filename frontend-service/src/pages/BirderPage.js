import React, { useContext, useState, useEffect } from 'react';
import SightingService from '../sighting/SightingService';
import { SightingsSection } from '../sighting/SightingsSection.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import { ApiContext } from 'api/ApiContext';
import './BirderPage.scss';
import 'birder/BirderConnectionButton.scss';

export default ({ birder }) => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const { account } = useContext(UserContext);
  const [sightings, setSightings] = useState([]);
  const { t } = useTranslation();

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
    <div className='birder-page'>
      <h1>{birder.name}</h1>
      {account.birder.id !== birder.id && <BirderConnectionButton birder={birder} />}
      <h2>{t('Sightings')}</h2>
      <SightingsSection sightings={sightings} />
    </div>
  );
};

const BirderConnectionButton = ({ birder }) => {
  const { authenticatedApiFetch } = useContext(ApiContext);
  const { account } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const [birderConnection, setBirderConnection] = useState(null);
  const { t } = useTranslation();
  const message = birderConnection !== null ? 'birder-connection-following-label' : 'birder-connection-no-connection-label';

  useEffect(() => {
    const resolveFollows = async () => {
      setLoading(true);
      const response = await authenticatedApiFetch(`/birders/${account.birder.id}/birder-connections`, {});
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
  }, [birder, account.birder.id]);

  const handleClick = e => {
    const updateBirderConnection = async () => {
      setLoading(true);
      if (birderConnection === null) {
        const response = await authenticatedApiFetch(`/birders/${account.birder.id}/birder-connections`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 'secondaryBirderId': birder.id })
        });
        if (response.status === 201) {
          const location = response.headers.get('Location');
          const response2 = await authenticatedApiFetch(location, {});
          if (response2.status === 200) {
            setBirderConnection(await response2.json());
          }
          else {
            setBirderConnection(null);
          }
        }
      }
      else {
        const response = await authenticatedApiFetch(`/birder-connections/${birderConnection.id}`, {
          method: 'DELETE',
        });
        if (response.status === 204) {
          setBirderConnection(null);
        }
      }
      setLoading(false);
    };
    updateBirderConnection();
  };

  const classNames = ['birder-connection-button'];
  if (birderConnection) {
    classNames.push('active');
  }

  return <button className={classNames.join(' ')} onClick={handleClick}>{loading ? '...' : t(message)}</button>;
};
