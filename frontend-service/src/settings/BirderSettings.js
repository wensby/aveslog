import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { FormGroup } from 'generic/FormGroup';
import { UserContext } from 'authentication/UserContext';
import { SubmitButton } from 'generic/form/SubmitButton';
import { ApiContext } from 'api/ApiContext';

export const BirderSettings = () => {
  const { authenticatedApiFetch } = useContext(ApiContext);
  const { account, patchBirder } = useContext(UserContext);
  const [name, setName] = useState(account.birder.name);
  const nameValid = /^[^\s]+(\s?[^\s]+)*$/.test(name);
  const { t } = useTranslation();

  const submit = async e => {
    e.preventDefault();
    if (nameValid) {
      const response = await authenticatedApiFetch(`/birders/${account.birder.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
        }),
      })
      if (response.status === 200) {
        const json = await response.json();
        patchBirder(json);
      }
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
