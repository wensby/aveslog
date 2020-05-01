import React, { useState, useContext } from 'react';
import { useTranslation } from 'react-i18next';
import { FormGroup } from 'generic/FormGroup';
import { UserContext } from 'authentication/UserContext';
import { AuthenticationContext } from 'authentication/AuthenticationContext';
import { SubmitButton } from 'generic/form/SubmitButton';

export const BirderSettings = () => {
  const { getAccessToken } = useContext(AuthenticationContext);
  const { account, patchBirder } = useContext(UserContext);
  const [name, setName] = useState(account.birder.name);
  const { t } = useTranslation();

  const submit = async e => {
    e.preventDefault();
    const token = await getAccessToken();
    const response = await fetch(`${window._env_.API_URL}/birders/${account.birder.id}`, {
      method: 'PATCH',
      headers: {
        accessToken: token.jwt,
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

  return (
    <section className='birder-settings'>
      <h2>{t('birder-label')}</h2>
      <form onSubmit={submit} className='birder-settings-form'>
        <FormGroup>
          <label htmlFor='name'>{t('name-label')}</label>
          <input id='name' type='text' placeholder={t('name-placeholder')}
            value={name} onChange={event => setName(event.target.value)} />
        </FormGroup>
        <SubmitButton>{t('save-birder-settings-button-label')}</SubmitButton>
      </form>
    </section>
  );
}
