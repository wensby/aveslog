import React from 'react';
import Button from 'react-bootstrap/Button';
import { SearchBar } from './SearchBar';
import { NavbarMain } from './NavbarMain';

export function NavbarConstant({ ref, onToggleNavbarClick }) {
  return (
    <div ref={ref} className='navbar-grid'>
      <NavbarMain />
      <div className='menu-button'>
        <Button onClick={onToggleNavbarClick} className='navbar-toggler'>
          <span className="navbar-toggler-icon"></span>
        </Button>
      </div>
      <div className='search-bar-item'>
        <SearchBar />
      </div>
    </div>
  );
}
