import React from 'react';

export function Menu({ onClick, items }) {

  const renderItem = (item, index) => {
    return (
      <div className="nav-item" key={index} onClick={onClick}>
        {item}
      </div>
    )
  };

  return (
    <div className='navbar-nav mr-auto' id='collapsableMenuList'>
      {items.map(renderItem)}
    </div>
  );
}
