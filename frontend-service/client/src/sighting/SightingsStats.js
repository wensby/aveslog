import React from 'react';
import { useTranslation } from 'react-i18next';
import { DisplayMode } from "./DisplayMode";

export function SightingsStats({ sightings, uniqueSelected, onUniqueSelectedChange }) {
  const { t } = useTranslation();
  return null;
}

function countUniqueBirds(sightings) {
  return new Set(sightings.map(sighting => sighting.birdId)).size;
}
