import React from 'react';
import { useMenuItems } from './useMenuItems.js';
import { MenuItem } from './menu/MenuItem.js';
import './Sidebar.scss';

export const Sidebar = () => {
  const menuItems = useMenuItems();

  return (
    <nav className='sidebar'>
      {menuItems.map((item, index) => <MenuItem item={item} key={index} />)}
    </nav>
  );
};
