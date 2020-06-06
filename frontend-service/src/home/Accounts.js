import React from 'react';
import { BirderLink } from './BirderLink';

export const Accounts = ({ accounts }) => {
  return accounts.map(account => (<BirderLink key={account.username} birder={account.birder} />));
};
