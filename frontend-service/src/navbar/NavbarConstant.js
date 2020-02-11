import React from 'react';
import { SearchBar } from './SearchBar';
import { NavbarMain } from './NavbarMain';

export const NavbarConstant = React.forwardRef(({ onToggleNavbarClick }, ref) => (
  <div ref={ref} className='navbar-grid'>
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
