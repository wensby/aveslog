import React, { useState } from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import { useReactRouter } from '../reactRouterHook';
import { useTranslation } from 'react-i18next';

export default () => {
  const { history } = useReactRouter();
  const [query, setQuery] = useState('');
  const { t } = useTranslation();

  const renderTextInput = () => {
    return (
      <Form.Control variant='light' aria-describedby='button-addon'
        name='query' placeholder={t('Search bird')} aria-label='Search bird'
        onChange={event => setQuery(event.target.value)}
        value={query}/>
    );
  };

  const renderButton = () => {
    return (
      <button variant="dark" className="rounded-0 btn btn-dark search-button"
        type="submit" id="button-addon">{t('Search')}</button>
    );
  };

  const onFormSubmit = event => {
    event.preventDefault();
    history.push(`/bird/search?q=${query}`);
    setQuery('');
  }

  return (
    <form id="birdSearchForm" onSubmit={onFormSubmit}>
      <InputGroup size="lg">
        {renderTextInput()}
        <InputGroup.Append>
          {renderButton()}
        </InputGroup.Append>
      </InputGroup>
    </form>
  );
}
