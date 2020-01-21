import { useState, useEffect } from 'react';
import birdRepository from './BirdRepository';
import { useTranslation } from 'react-i18next';

export function useBird(birdId) {
  const [bird, setBird] = useState(null);
  const [error, setError] = useState(null);

  const resolveBird = async () => {
    const bird = await birdRepository.getBird(birdId);
    if (bird) {
      setBird(bird);
    }
    else {
      setError('missing');
    }
  }

  useEffect(() => {
    resolveBird();
  }, []);

  return { bird, error };
}

export function useBirdName(bird) {
  const { i18n } = useTranslation();
  if (bird) {
    const language = i18n.languages[0];
    const local = bird.names && bird.names[language] ? bird.names[language] : null;
    const binomial = bird.binomialName;
    return { local, binomial };
  }
  else {
    return { local: null, binomial: null };
  }
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
