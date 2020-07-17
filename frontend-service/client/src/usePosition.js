import { useState, useEffect } from 'react';

export const usePosition = (enabled) => {
  const [position, setPosition] = useState({});
  const [error, setError] = useState(null);

  const onChange = ({coords}) => {
    setPosition({
      latitude: coords.latitude,
      longitude: coords.longitude,
    })
  };

  const onError = (error) => {
    setError(error.message);
  };

  useEffect(() => {
    if (enabled) {
      const geo = navigator.geolocation;
      if (!geo) {
        setError('Geolocation is not supported');
        return;
      }
      const watcher = geo.watchPosition(onChange, onError);
      return () => geo.clearWatch(watcher);
    }
    else {
      setPosition({});
      setError(null);
    }
  }, [enabled]);

  return {...position, error}
}
