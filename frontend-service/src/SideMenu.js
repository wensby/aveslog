import React from 'react';
import { Link } from 'react-router-dom';
import { useMenuItems } from './useMenuItems.js';
import './SideMenu.scss';

export const SideMenu = () => {
  const items = useMenuItems();

  const renderItem = (item, index) => {
    return (
      <div className='nav-item' key={index}>
        <Link className='nav-link' to={item.link} onClick={item.action}>{item.label}</Link>
      </div>
    );
  };

  return (
    <div className='sidemenu'>
      <nav className='sidebar'>
        {items.map(renderItem)}
      </nav>
    </div>
  );
};
