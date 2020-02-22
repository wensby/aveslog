import { useState, useEffect } from 'react';
import birdRepository from './BirdRepository';
import { useTranslation } from 'react-i18next';

export function useBird(birdId) {
  const [bird, setBird] = useState(null);
  const [error, setError] = useState(null);
  const apiUrl = window._env_.API_URL;
  const url = `${apiUrl}/birds/${birdId}?embed=commonNames`;

  useEffect(() => {
    const resolveBird = async () => {
      const response = await fetch(url);
      if (response.status === 200) {
        setBird(await response.json());
      }
      else {
        setError('missing');
      }
    }
    resolveBird();
  }, [birdId, url]);

  return { bird, error };
}

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
