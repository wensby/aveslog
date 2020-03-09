import React from 'react';
import { useMenuItems } from './useMenuItems.js';
import { Link } from 'react-router-dom';
import './Sidebar.scss';

export const Sidebar = () => {
  const menuItems = useMenuItems();

  return (
    <nav className='sidebar'>
      {menuItems.map((item, index) => <MenuItem item={item} key={index} />)}
    </nav>
  );
};

const MenuItem = ({ item }) => {
  if (item.link) {
    return <Link to={item.link} onClick={item.action}>{item.label}</Link>;
  }
  else {
    return <div onClick={item.action}>{item.label}</div>
  }
}
