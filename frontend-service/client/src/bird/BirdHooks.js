import { useState, useEffect, useContext } from 'react';
import birdRepository from './BirdRepository';
import { useTranslation } from 'react-i18next';
import { BirdsContext } from './BirdsContext';

export const useBird = birdId => {
  const { addBird } = useContext(BirdsContext);
  const [bird, setBird] = useState(null);
  const birdPromise = useBirdPromise(birdId);
  const contextBird = useContextBird(birdId);

  useEffect(() => {
    if (contextBird) {
      setBird(contextBird);
    }
  }, [contextBird]);

  useEffect(() => {
    const resolveBirdPromise = async promise => {
      const response = await promise;
      if (response.status === 200 && !response.bodyUsed) {
        const bird = await response.json();
        addBird(bird);
      }
    };
    if (birdPromise) {
      resolveBirdPromise(birdPromise);
    }
  }, [birdPromise, addBird]);

  return { bird, error: null };
};

/**
 * Returns previously fetched bird BirdsContext, but refreshes the bird it is
 * urgent that we have a bird.
 * @param {*} id the id of the bird
 * @param {*} eager true if it is urgent that we get a fresh state of the bird
 */
export const useLazyBird = (id, eager) => {
  const { addBird } = useContext(BirdsContext);
  const [bird, setBird] = useState(null);
  const contextBird = useContextBird(id);

  useEffect(() => {
    if(bird && bird.id !== id) {
      setBird(null);
    }
  }, [id, bird]);

  useEffect(() => {
    setBird(contextBird);
  }, [contextBird]);

  useEffect(() => {
    const resolveBirdPromise = async () => {
      const promise = fetch(`/api/birds/${id}?embed=commonNames`);
      const response = await promise;
      if (response.status === 200 && !response.bodyUsed) {
        const bird = await response.json();
        addBird(bird);
      }
    };
    if (eager) {
      resolveBirdPromise();
    }
  }, [id, eager, addBird]);

  return bird;
}

export const useContextBird = birdId => {
  const { birds } = useContext(BirdsContext);
  return birds.has(birdId) ? birds.get(birdId) : null;
};

const useBirdPromise = birdId => {
  const [promise, setPromise] = useState(null);

  useEffect(() => {
    setPromise(fetch(`/api/birds/${birdId}?embed=commonNames`));
  }, [birdId]);

  return promise;
};

export function useCommonName(bird) {
  const [loading, setLoading] = useState(true);
  const [commonName, setCommonName] = useState(null);
  const { i18n } = useTranslation();
  const language = i18n.languages[0];

  useEffect(() => {
    const resolveCommonName = async () => {
      setLoading(true);
      const url = `/api/birds/${bird.id}/common-names?locale=${language}`;
      const response = await fetch(url);
      if (response.status === 200) {
        const json = await response.json();
        if (json.items.length > 0) {
          setCommonName(json.items[0].name);
        }
        else {
          setCommonName(null);
        }
      }
      else {
        setCommonName(null);
      }
      setLoading(false);
    };
    setCommonName(null);
    if (bird && bird.commonNames) {
      const result = bird.commonNames.filter(commonName => commonName.locale === language);
      if (result.length > 0) {
        setCommonName(result[0].name);
        setLoading(false);
        return;
      }
    }
    else if (bird) {
      resolveCommonName();
    }
  }, [bird, language]);

  return { commonName, loading };
}

export function useBirdStatistics(bird) {
  const [statistics, setStatistics] = useState({});

  useEffect(() => {
    const fetchStatistics = async bird => {
      const id = bird.binomialName.toLowerCase().replace(' ', '-');
      const stats = await birdRepository.getBirdStatistics(id);
      setStatistics(stats);
    }
    if (bird) {
      fetchStatistics(bird);
    }
  }, [bird]);

  return statistics;
}

export function useCommonNames(bird, forceReload) {
  const [names, setNames] = useState([]);
  const url = `/api/birds/${bird.id}/common-names`;

  useEffect(() => {
    const resolveNames = async () => {
      const response = await fetch(url);
      if (response.status === 200) {
        setNames((await response.json()).items);
      }
    };
    if (bird) {
      resolveNames();
    }
  }, [bird, url]);

  useEffect(() => {
    const resolveNames = async () => {
      const response = await fetch(url, { cache: 'reload' });
      if (response.status === 200) {
        setNames((await response.json()).items);
      }
    };
    if (forceReload) {
      resolveNames();
    }
  }, [forceReload, url]);

  return names;
}
