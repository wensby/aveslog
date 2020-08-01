import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import axios from 'axios';

export function CommonNameForm({ bird, locales, onNameAdded }) {
  const [selectedLanguage, setSelectedLangauge] = useState(null);
  const [name, setName] = useState('');
  const { t } = useTranslation();

  useEffect(() => {
    setSelectedLangauge(locales[0]);
  }, [locales]);

  const onLanguageChange = event => {
    setSelectedLangauge(event.target.value);
  };

  const handleSubmit = event => {
    const postName = async (langauge, name) => {
      const response = await postCommonName(bird, langauge, name);
      if (response.status === 201) {
        onNameAdded(langauge, name);
        setName('');
      }
    }
    event.preventDefault();
    postName(selectedLanguage, name);
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

const postCommonName = async (bird, language, name) => {
  return axios.post(`/api/birds/${bird.id}/common-names`, {
    'locale': language,
    'name': name
  });
};
