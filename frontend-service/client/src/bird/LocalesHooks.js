import { useState, useEffect } from 'react';

export function useLocales() {
  const [locales, setLocales] = useState([]);

  useEffect(() => {
    const resolveLocales = async () => {
      const response = await fetch('/api/locales');
      if (response.status === 200) {
        setLocales((await (response.json())).items);
      }
    };
    resolveLocales();
  }, []);
  
  return locales;
}
