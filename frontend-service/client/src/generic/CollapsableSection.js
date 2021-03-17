import React, { useState } from 'react';
import Icon from 'Icon';
import './CollapsableSection.scss';

export const CollapsableSection = ({ children }) => {
  const [state, setState] = useState('collapsed');

  const toggleState = () => {
    if (state === 'collapsed') setState('expanded');
    else setState('collapsed');
  }

  return (
    <div className={`collapsable-section ${state}`}>
      <div className='toggle' onClick={() => toggleState()}><Icon name='down'></Icon></div>
      {children}
    </div>
  );
};
