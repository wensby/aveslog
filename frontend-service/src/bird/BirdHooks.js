import { useState, useEffect, useContext } from 'react';
import birdRepository from './BirdRepository';
import { useTranslation } from 'react-i18next';
import { BirdsContext } from './BirdsContext';

export const useBird = birdId => {
  const { birds, addBird } = useContext(BirdsContext);
  const [bird, setBird] = useState(null);
  const [loading, setLoading] = useState(null);
  const birdPromise = useBirdPromise(birdId);

  useEffect(() => {
    const correctBirdState = bird && bird.id === birdId;
    if (!loading && !correctBirdState && birdId in birds) {
      setBird(birds[birdId]);
    }
  }, [birdId, birds, bird, loading]);

  useEffect(() => {
    const resolveBirdPromise = async promise => {
      setLoading(true);
      const response = await promise;
      if (response.status === 200 && !response.bodyUsed) {
        addBird(await response.json());
      }
      setLoading(false);
    };
    if (birdPromise) {
      resolveBirdPromise(birdPromise);
    }
  }, [birdPromise]);

  return { bird, error: null };
};

const useBirdPromise = birdId => {
  const [promise, setPromise] = useState(null);

  useEffect(() => {
    const apiUrl = window._env_.API_URL;
    setPromise(fetch(`${apiUrl}/birds/${birdId}?embed=commonNames`));
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
      const apiUrl = window._env_.API_URL;
      const url = `${apiUrl}/birds/${bird.id}/common-names?locale=${language}`;
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
    if (bird.commonNames) {
      const result = bird.commonNames.filter(commonName => commonName.locale === language);
      if (result.length > 0) {
        setCommonName(result[0].name);
        setLoading(false);
        return;
      }
    }
    resolveCommonName();
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
  const apiUrl = window._env_.API_URL;
  const url = `${apiUrl}/birds/${bird.id}/common-names`;

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
