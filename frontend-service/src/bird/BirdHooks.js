import React, { useState, useEffect } from 'react';
import birdRepository from './BirdRepository';
import { useTranslation } from 'react-i18next';

export function useBird(birdId) {
  const [bird, setBird] = useState(null);

  const resolveBird = async () => {
    const bird = await birdRepository.getBird(birdId);
    setBird(bird);
  }

  useEffect(() => {
    resolveBird();
  });

  return bird;
}
