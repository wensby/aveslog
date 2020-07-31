import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { FormGroup } from 'generic/FormGroup';
import { UserContext } from 'authentication/UserContext';
import { SubmitButton } from 'generic/form/SubmitButton';
import axios from 'axios';

export const BirderSettings = () => {
  const { account, patchBirder } = useContext(UserContext);
  const [name, setName] = useState(account.birder.name);
  const nameValid = /^[^\s]+(\s?[^\s]+)*$/.test(name);
  const { t } = useTranslation();

  const submit = e => {
    e.preventDefault();
    if (nameValid) {
      axios.patch(`/api/birders/${account.birder.id}`, {
        name: name,
      })
        .then(response => patchBirder(response.data));
    }
  }

  const classNames = [];
  if (!nameValid) {
    classNames.push('is-invalid');
  }
  else {
    classNames.push('is-valid');
  }

  return (
    <section className='birder-settings'>
      <h2>{t('birder-label')}</h2>
      <form onSubmit={submit} className='birder-settings-form'>
        <FormGroup>
          <label htmlFor='name'>{t('name-label')}</label>
          <input className={classNames.join(' ')}
            id='name' type='text' placeholder={t('name-placeholder')}
            value={name} onChange={event => setName(event.target.value)} />
        </FormGroup>
        <SubmitButton disabled={!nameValid || account.birder.name === name}>
          {t('save-birder-settings-button-label')}
        </SubmitButton>
      </form>
    </section>
  );
}
