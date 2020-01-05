import React, { useState, useEffect } from 'react';
import './style.scss';

export function ToggleButtonGroup({onSelected, children}) {
  const [selectedTab, setSelectedTab] = useState(null);

  useEffect(() => {
    onSelected(selectedTab);
  }, [selectedTab]);

  return (
    <div class='toggle-button-group'>
      {children.map(child => React.cloneElement(child, {
        selected: selectedTab,
        onSelected: setSelectedTab
      }))}
    </div>
  );
}
