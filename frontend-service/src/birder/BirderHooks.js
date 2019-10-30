import React, { useContext, useState, useEffect } from 'react';
import { UserContext } from '../authentication/UserContext';
import birderRepository from './BirderRepository';

export function useBirder(birderId) {
  const { getAccessToken } = useContext(UserContext);
  const [birder, setBirder] = useState(null);

  const resolveBirder = async () => {
    const token = await getAccessToken();
    const birder = await birderRepository.getBirder(birderId, token);
    setBirder(birder);
  }

  useEffect(() => {
    resolveBirder();
  }, [birderId]);

  return birder;
}
