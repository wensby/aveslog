import React from 'react';
import { useMenuItems } from './useMenuItems.js';
import { Link } from 'react-router-dom';
import './Sidebar.scss';

export const Sidebar = () => {
  const items = useMenuItems();

  return (
    <nav className='sidebar'>
      {items.map(renderItem)}
    </nav>
  );
};

const renderItem = (item, index) => {
  if (item.link) {
    return <Link key={index} className='nav-link' to={item.link} onClick={item.action}>{item.label}</Link>;
  }
  else {
    return <div key={index} className='nav-link' onClick={item.action}>{item.label}</div>
  }
};
