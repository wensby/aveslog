import React, { useEffect, useState } from 'react';
import { useAuthentication } from '../authentication/AuthenticationHooks.js';
import axios from 'axios';

export const FollowedBirdersContainer = () => {
  const [followedBirders, setFollowedBirders] = useState([]);
  const { account } = useAuthentication();

  useEffect(() => {
    const resolveBirderConnections = async () => {
      const response = await axios.get(`/api/birders/${account.birder.id}/birder-connections`);
      if (response.status === 200) {
        const json = response.data;
        setFollowedBirders(json.items);
      }
    };
    resolveBirderConnections();
  }, [account]);

  return <FollowedBirders followedBirders={followedBirders} />;
};

const FollowedBirders = ({ followedBirders }) => {
  return (
    <div>
      {followedBirders.map(f => <div>{f.secondaryBirderId}</div>)}
    </div>
  );
}
