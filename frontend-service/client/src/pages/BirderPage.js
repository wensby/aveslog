import React, { useContext, useState, useEffect } from 'react';
import { SightingsSection } from '../sighting/SightingsSection.js';
import { UserContext } from '../authentication/UserContext';
import { useTranslation } from 'react-i18next';
import './BirderPage.scss';
import 'birder/BirderConnectionButton.scss';
import { PageHeading } from 'generic/PageHeading';
import axios from 'axios';

export default ({ data }) => {
  const { account } = useContext(UserContext);
  const { t } = useTranslation();

  return (
    <div className='birder-page'>
      <PageHeading>{data.birder.name}</PageHeading>
      {account.birder.id !== data.birder.id && <BirderConnectionButton birder={data.birder} />}
      <h2>{t('Sightings')}</h2>
      <SightingsSection sightings={data.sightings.items} />
    </div>
  );
};

const BirderConnectionButton = ({ birder }) => {
  const { account } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const [birderConnection, setBirderConnection] = useState(null);
  const { t } = useTranslation();
  const message = birderConnection !== null ? 'birder-connection-following-label' : 'birder-connection-no-connection-label';

  useEffect(() => {
    const resolveFollows = async () => {
      setLoading(true);
      const response = await axios.get(`/api/birders/${account.birder.id}/birder-connections`);
      if (response.status === 200) {
        const json = response.data;
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
        const response = await axios.post(`/api/birders/${account.birder.id}/birder-connections`, {
          'secondaryBirderId': birder.id
        });
        if (response.status === 201) {
          const location = response.headers.get('Location');
          const response2 = await axios.get('/api' + location);
          if (response2.status === 200) {
            setBirderConnection(response2.data);
          }
          else {
            setBirderConnection(null);
          }
        }
      }
      else {
        const response = await axios.delete(`/api/birder-connections/${birderConnection.id}`);
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
