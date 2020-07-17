import React from 'react';
import './Alert.scss';

export const Alert = ({ type, message }) => {
  return <div className={`alert alert-${type}`} role='alert'>{message}</div>;
};
