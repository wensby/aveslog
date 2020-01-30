import { useState, useEffect } from 'react';
import birdRepository from './BirdRepository';
import { useTranslation } from 'react-i18next';

export function useBird(birdId) {
  const [bird, setBird] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const resolveBird = async () => {
      const bird = await birdRepository.getBird(birdId);
      if (bird) {
        setBird(bird);
      }
      else {
        setError('missing');
      }
    }
    resolveBird();
  }, [birdId]);

  return { bird, error };
}

export function useBirdName(bird) {
  const [name, setName] = useState(null);
  const { i18n } = useTranslation();
  const language = i18n.languages[0];
  const apiUrl = window._env_.API_URL;
  const url = `${apiUrl}/birds/${bird.id}/common-names?locale=${language}`;

  useEffect(() => {
    const resolveCommonName = async () => {
      const response = await fetch(url);
      if (response.status === 200) {
        const json = await response.json();
        if (json.items.length > 0) {
          setName(json.items[0].name);
        }
        else {
          setName(null);
        }
      }
      else {
        setName(null);
      }
    };
    resolveCommonName();
  }, [bird, language, url]);
  
  return { local: name, binomial: bird ? bird.binomialName : null };
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
