import React from 'react';
import { BirderLink } from './BirderLink';

export const BirdersList = ({ birders }) => {
  return birders.map(birder => (<BirderLink key={birder.id} birder={birder} />));
};
