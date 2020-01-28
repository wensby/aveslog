import React, { useState, useRef, useEffect, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import Icon from '../Icon.js';
import './CommonNameAdder.scss';
import { UserContext } from '../authentication/UserContext';

export function CommonNameAdder({ birdId, locales, onNameAdded }) {
  const { getAccessToken } = useContext(UserContext);
  const [expanded, setExpanded] = useState(false);
  const { t } = useTranslation();
  const [selectedLanguage, setSelectedLangauge] = useState(null);
  const [name, setName] = useState('');
  const wrapperRef = useRef(null);
  useOutsideAlerter(wrapperRef, () => { setExpanded(false) });
  const activate = e => {
    e.preventDefault();
    setExpanded(true);
  };

  useEffect(() => {
    setSelectedLangauge(locales[0]);
  }, [locales])

  const handleSubmit = event => {
    const postName = async name => {
      const accessToken = await getAccessToken();
      const response = await fetch(`${window._env_.API_URL}/birds/${birdId}/common-names`, {
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
        setExpanded(false);
      }
    }
    event.preventDefault();
    postName(name);
  };

  const onLanguageChange = event => {
    setSelectedLangauge(event.target.value);
  }

  if (expanded) {
    return (
      <div ref={wrapperRef} className={'common-name-adder' + (expanded ? ' expanded' : '')}>
        <form onSubmit={handleSubmit}>
          <select value={selectedLanguage} onChange={onLanguageChange}>
            {locales.map(l => <option value={l}>{l.toUpperCase()}</option>)}
          </select>
          <input value={name} type='text' onChange={event => setName(event.target.value)} />
          <button type='submit'>{t('add-button')}</button>
        </form>
      </div>
    );
  }
  else {
    return (
      <div className='common-name-adder' onClick={activate} >
        <Icon name='add' />
      </div>
    );
  }
}

function useOutsideAlerter(ref, onClickOutside) {
  function handleClickOutside(event) {
    if (ref.current && !ref.current.contains(event.target)) {
      onClickOutside();
    }
  }

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  });
}
