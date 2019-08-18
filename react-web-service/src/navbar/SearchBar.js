import React from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useTranslation } from "react-i18next";

export default function SearchBar() {

  const { t } = useTranslation();

  const renderTextInput = () => {
    return (
      <Form.Control variant='light' aria-describedby='button-addon'
        name='query' placeholder={t('Search bird')} aria-label='Search bird' />
    );
  };

  const renderButton = () => {
    return (
      <Button variant="light" className="rounded-0" type="submit"
        id="button-addon">{t('Search')}</Button>);
  };

  return (
    <Form id="birdSearchForm" action="/bird/search" method="get">
      <InputGroup size="lg">
        {renderTextInput()}
        <InputGroup.Append>
          {renderButton()}
        </InputGroup.Append>
      </InputGroup>
    </Form>
  );
}
