import { useState, useEffect } from 'react';
import { useTranslation } from "react-i18next";

export const usePositionName = (location) => {
  const { i18n } = useTranslation();
  const language = i18n.languages[0];
  const [name, setName] = useState('');

  useEffect(() => {
    const fetchLocationName = async (latitude, longitude) => {
      const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=21&addressdetails=1&accept-language=${language}`);
      if (response.status == 200) {
        const json = await response.json();
        setName(json.display_name);
      }
    }
    if (location) {
      fetchLocationName(location[0], location[1]);
    }
    else {
      setName('');
    }
  }, [location, language]);

  return name
}
