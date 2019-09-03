import React, { useState } from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
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
      <Button variant="light" className="rounded-0" type="submit"
        id="button-addon">{t('Search')}</Button>
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
