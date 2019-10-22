import React from 'react';
import Nav from 'react-bootstrap/Nav';
import './style.scss';

export default ({ onClick, items }) => {

  const renderItem = (item, index) => {
    return (
      <div className="nav-item" key={index} onClick={onClick}>
        {item}
      </div>
    )
  };

  return (
    <Nav className='navbar-nav mr-auto' id='collapsableMenuList'>
      {items.map(renderItem)}
    </Nav>
  );
}
