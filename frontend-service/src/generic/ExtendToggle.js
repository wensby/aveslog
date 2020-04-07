import React from 'react';
import Icon from 'Icon.js';
import './ExtendToggle.scss';

export const ExtendToggle = ({ active, onChange }) => {
  const click = event => {
    event.preventDefault();
    onChange(!active);
  };

  return (
    <div className={className(active)} onClick={click}>
      <Icon name='down' />
    </div>
  );
};

function className(active) {
  const classNames = ['extend-toggle'];
  if (active) {
    classNames.push('extended');
  }
  return classNames.join(' ');
}

