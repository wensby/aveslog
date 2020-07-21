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

export const useBirderPage = id => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const accessToken = await getAccessToken();
      const response = await fetch(`/api/birder-page/${id}`, {
        headers: {
          'accessToken': accessToken.jwt,
        },
      });
      if (response.status === 200) {
        setData(await response.json());
      }
      setLoading(false);
    }
    fetchData();
  }, [id, getAccessToken]);

  return { data, loading }
}
