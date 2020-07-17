import React from 'react';
import './CommonNameItem.scss';

export function CommonNameItem({ code, name, ...props }) {
  return (
    <div className='common-name-item' {...props}>
      <div>{code}</div>
      <div>{name}</div>
    </div>
  );
}
