import React from 'react';
import { NavbarMain } from './NavbarMain';
import { NavbarToggler} from './NavbarToggler.js';
import { SearchBar } from './search/SearchBar.js';
import './NavbarConstant.scss';

export const NavbarConstant = React.forwardRef((props, ref) => (
  <div ref={ref} className='navbar-constant'>
    <NavbarMain />
    <div className='menu-button'>
      <NavbarToggler />
    </div>
    <SearchBar />
  </div>
));
