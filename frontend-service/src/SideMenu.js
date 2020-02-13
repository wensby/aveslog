import React from 'react';
import { useMenuItems } from './useMenuItems.js';
import './SideMenu.scss';

export const SideMenu = () => {
  const items = useMenuItems();

  const renderItem = (item, index) => {
    return <div className="nav-item" key={index}>{item}</div>;
  };

  return (
    <div className="sidemenu">
      <nav className="sidebar nav flex-column border-left" id="sidebarList">
        {items.map(renderItem)}
      </nav>
    </div>
  );
};
