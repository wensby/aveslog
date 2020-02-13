import React from 'react';
import { SearchBar } from './SearchBar';
import { NavbarMain } from './NavbarMain';
import { NavbarToggler} from './NavbarToggler.js';
import './NavbarConstant.scss';

export const NavbarConstant = React.forwardRef(({ onToggleNavbarClick }, ref) => (
  <div ref={ref} className='navbar-constant'>
    <NavbarMain />
    <div className='menu-button'>
      <NavbarToggler onClick={onToggleNavbarClick}/>
    </div>
    <div className='search-bar-item'>
      <SearchBar />
    </div>
  </div>
));
