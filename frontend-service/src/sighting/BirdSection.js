import React from 'react';
import { useTranslation } from "react-i18next";
import { Label } from './Label';

export function BirdSection({ bird }) {
  const { i18n } = useTranslation();
  const language = i18n.languages[0];
  const name = bird.names && bird.names[language] ? bird.names[language] : bird.binomialName;

  return (
    <div className='form-group row'>
      <Label htmlFor='birdInput' label='bird-label' />
      <div className='col-sm-10'>
        <input id='birdInput' type='text' readOnly className='col-sm-10 form-control-plaintext' value={name} />
      </div>
    </div>
  );
}
