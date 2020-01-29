import React, { useState, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { UserContext } from '../authentication/UserContext';

export function CommonNameForm({ bird, locales, onNameAdded }) {
  const [selectedLanguage, setSelectedLangauge] = useState(null);
  const [name, setName] = useState('');
  const { getAccessToken } = useContext(UserContext);
  const { t } = useTranslation();

  useEffect(() => {
    setSelectedLangauge(locales[0]);
  }, [locales]);

  const onLanguageChange = event => {
    setSelectedLangauge(event.target.value);
  };

  const handleSubmit = event => {
    const postName = async (name) => {
      const accessToken = await getAccessToken();
      const response = await fetch(`${window._env_.API_URL}/birds/${bird.id}/common-names`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'accessToken': accessToken.jwt
        },
        body: JSON.stringify({
          'locale': selectedLanguage,
          'name': name
        }),
      });
      if (response.status === 201) {
        onNameAdded();
        setName('');
      }
    };
    event.preventDefault();
    postName(name);
  };

  return (
    <form onSubmit={handleSubmit}>
      <select value={selectedLanguage} onChange={onLanguageChange}>
        {locales.map(l => <option value={l}>{l.toUpperCase()}</option>)}
      </select>
      <input value={name} type='text' onChange={event => setName(event.target.value)} />
      <button type='submit'>{t('add-button')}</button>
    </form>
  );
}
