import { useContext, useState, useEffect } from 'react';
import { UserContext } from '../authentication/UserContext';
import birderRepository from './BirderRepository';

export function useBirder(birderId) {
  const { accessToken } = useContext(UserContext);
  const [birder, setBirder] = useState(null);  

  useEffect(() => {
    const resolveBirder = async () => {
      const birder = await birderRepository.getBirder(birderId, accessToken);
      setBirder(birder);
    }
    resolveBirder();
  }, [birderId]);

  return birder;
}
