import React, { useEffect, useState, useContext } from 'react';
import { useAuthentication } from '../authentication/AuthenticationHooks.js';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';

export const FollowedBirdersContainer = () => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [followedBirders, setFollowedBirders] = useState([]);
  const { account } = useAuthentication();

  useEffect(() => {
    const resolveBirderConnections = async () => {
      const accessToken = await getAccessToken();
      const response = await fetch(`${window._env_.API_URL}/birders/${account.birder.id}/birder-connections`, {
        headers: {
          'accessToken': accessToken.jwt,
        }
      });
      if (response.status === 200) {
        const json = await response.json();
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
