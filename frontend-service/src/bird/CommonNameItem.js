import React from 'react';
import './CommonNameItem.scss';

export function CommonNameItem({ code, name, ...props }) {
  return (
    <div className='common-name-item' {...props}>
      <span>{code}</span>
      <span>{name}</span>
    </div>
  );
}
