import { useState, useEffect } from 'react';
import axios from 'axios';

export function useLocales() {
  const [locales, setLocales] = useState([]);

  useEffect(() => {
    const resolveLocales = async () => {
      const response = await axios.get('/api/locales');
      if (response.status === 200) {
        setLocales(response.data.items);
      }
    };
    resolveLocales();
  }, []);
  
  return locales;
}
