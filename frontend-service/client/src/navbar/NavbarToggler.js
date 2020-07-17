import React, { useContext } from 'react';
import './NavbarToggler.scss';
import { NavbarContext } from './Navbar.js';

export const NavbarToggler = () => {
  const { toggleNavbar } = useContext(NavbarContext);

  return (
    <button onClick={toggleNavbar} className='navbar-toggler'>
      <span className="navbar-toggler-icon"></span>
    </button>
  );
};
