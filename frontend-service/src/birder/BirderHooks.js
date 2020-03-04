import { useContext, useState, useEffect } from 'react';
import { UserContext } from '../authentication/UserContext';
import birderRepository from './BirderRepository';

export function useBirder(birderId) {
  const { getAccessToken } = useContext(UserContext);
  const [birder, setBirder] = useState(null);  

  useEffect(() => {
    const resolveBirder = async () => {
      const accessToken = getAccessToken();
      if (accessToken) {
        const birder = await birderRepository.getBirder(birderId, accessToken);
        setBirder(birder);
      }
    }
    resolveBirder();
  }, [birderId, getAccessToken]);

  return birder;
}
