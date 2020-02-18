import React from 'react';
import { Link } from 'react-router-dom';
import { useMenuItems } from './useMenuItems.js';
import './SideMenu.scss';

export const SideMenu = () => {
  const items = useMenuItems();

  const renderItem = (item, index) => {
    return <Link className='nav-link' key={index} to={item.link} onClick={item.action}>{item.label}</Link>;
  };

  return (
    <div className='sidemenu'>
      <nav className='sidebar'>
        {items.map(renderItem)}
      </nav>
    </div>
  );
};
