import React from 'react';
import { Link } from "react-router-dom";
import { Brand } from 'specific/Brand.js';
import './NavbarBrand.scss';

export const NavbarBrand = () => (
  <div className='navbar-brand'>
    <Link to='/home' className='text-decoration-none'>
      <Brand />
    </Link>
  </div>
);
