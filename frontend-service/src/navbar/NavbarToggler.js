import React from 'react';
import './NavbarToggler.scss';

export const NavbarToggler = ({ onClick }) => {
  return (
    <button onClick={onClick} className='navbar-toggler'>
      <span className="navbar-toggler-icon"></span>
    </button>
  );
};
