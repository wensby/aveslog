import React from 'react';
import './CommonNameItem.scss';

export function CommonNameItem({ code, name }) {
  return (
    <div className='common-name-item'>
      <span>{code}</span>
      <span>{name}</span>
    </div>
  );
}
