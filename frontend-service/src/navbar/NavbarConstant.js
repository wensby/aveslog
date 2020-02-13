import React from 'react';
import { SearchBar } from './SearchBar';
import { NavbarMain } from './NavbarMain';
import './NavbarConstant.scss';

export const NavbarConstant = React.forwardRef(({ onToggleNavbarClick }, ref) => (
  <div ref={ref} className='navbar-constant'>
    <NavbarMain />
    <div className='menu-button'>
      <button onClick={onToggleNavbarClick} className='navbar-toggler'>
        <span className="navbar-toggler-icon"></span>
      </button>
    </div>
    <div className='search-bar-item'>
      <SearchBar />
    </div>
  </div>
));
