import { useContext, useState, useEffect } from 'react';
import birderRepository from './BirderRepository';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export function useBirder(birderId) {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [birder, setBirder] = useState(null);  

  useEffect(() => {
    const resolveBirder = async () => {
      const accessToken = await getAccessToken();
      if (accessToken) {
        const birder = await birderRepository.getBirder(birderId, accessToken);
        setBirder(birder);
      }
    }
    resolveBirder();
  }, [birderId, getAccessToken]);

  return birder;
}
