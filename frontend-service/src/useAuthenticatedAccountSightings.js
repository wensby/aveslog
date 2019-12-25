import { useEffect, useContext } from 'react';
import { SightingContext } from './sighting/SightingContext';

export const useAuthenticatedAccountSightings = () => {
  const { sightings, refreshSightings } = useContext(SightingContext);
  useEffect(() => {
    refreshSightings();
  }, []);
  return sightings
}
