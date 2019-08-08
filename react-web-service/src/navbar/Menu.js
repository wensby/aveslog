import React from 'react';
import Nav from 'react-bootstrap/Nav';
import './navbar.css';

export default function Menu(props) {

  const renderItem = (item, index) => {
    return (
      <div className="nav-item" key={index} onClick={props.onClick}>
        {item}
      </div>
    )
  };

  return (
    <Nav className='navbar-nav mr-auto' id='collapsableMenuList'>
      {props.items.map(renderItem)}
    </Nav>
  );
}