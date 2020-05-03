import React from 'react';
import './SubmitButton.scss';

export const SubmitButton = ({ children, disabled }) =>
  <button disabled={disabled} className='submit-button'>
    {children}
  </button>;

