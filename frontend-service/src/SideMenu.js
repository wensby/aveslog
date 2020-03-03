import React from 'react';
import { Link } from 'react-router-dom';
import { useMenuItems } from './useMenuItems.js';
import './SideMenu.scss';

export const SideMenu = () => {
  const items = useMenuItems();

  const renderItem = (item, index) => {
    if (item.link) {
      return <Link key={index} className='nav-link' to={item.link} onClick={item.action}>{item.label}</Link>;
    }
    else {
      return <div key={index} className='nav-link' onClick={item.action}>{item.label}</div>
    }
  };

  return (
    <div className='sidemenu'>
      <nav className='sidebar'>
        {items.map(renderItem)}
      </nav>
    </div>
  );
};
