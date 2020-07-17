import React from 'react';
import './ToggleButton.scss';

export function ToggleButton({ value, selected, disabled, onSelected, children }) {
  var className;
  if (selected === value) {
    className = 'toggle-button selected';
  }
  else {
    className = 'toggle-button';
  }
  const onClick = e => {
    e.preventDefault();
    if (selected === value) {
      onSelected(null);
    }
    else {
      onSelected(value);
    }
  };
  return <button className={className} disabled={disabled} onClick={onClick}>{children}</button>;
}
