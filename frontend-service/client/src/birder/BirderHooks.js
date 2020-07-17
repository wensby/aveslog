import { useContext, useState, useEffect } from 'react';
import birderRepository from './BirderRepository';
import { AuthenticationContext } from '../authentication/AuthenticationContext';

export function useBirder(birderId) {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [birder, setBirder] = useState(null);  
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const resolveBirder = async () => {
      setLoading(true);
      const accessToken = await getAccessToken();
      if (accessToken) {
        const birder = await birderRepository.getBirder(birderId, accessToken);
        setBirder(birder);
      }
      setLoading(false);
    }
    resolveBirder();
  }, [birderId, getAccessToken]);

  return { birder, loading };
}
