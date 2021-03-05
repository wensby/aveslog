import { useState, useEffect } from 'react';
import birderRepository from './BirderRepository';
import axios from 'axios';

export function useBirder(birderId) {
  const [birder, setBirder] = useState(null);  
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const resolveBirder = async () => {
      setLoading(true);
      const birder = await birderRepository.getBirder(birderId);
      setBirder(birder);
      setLoading(false);
    }
    resolveBirder();
  }, [birderId]);

  return { birder, loading };
}

export const useBirderPage = id => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const response = await axios.get(`/api/birder-page/${id}`);
      if (response.status === 200) {
        setData(response.data);
      }
      setLoading(false);
    }
    fetchData();
  }, [id]);

  return { data, loading }
}
