import React from 'react';
import { Link } from 'react-router-dom';

export function Menu({ onClick, items }) {

  const renderItem = (item, index) => {
    if (item.link) {
      return <Link key={index} className='nav-link' to={item.link} onClick={item.action}>{item.label}</Link>;
    }
    else {
      return <div key={index} className='nav-link' onClick={item.action}>{item.label}</div>
    }
  };

  return (
    <div className='navbar-nav mr-auto' id='collapsableMenuList' onClick={onClick}>
      {items.map(renderItem)}
    </div>
  );
}
