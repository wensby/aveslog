import React from 'react';
import { Link } from "react-router-dom";
import './NavbarBrand.scss';

export const NavbarBrand = () => (
  <div className='navbar-brand'>
    <Link to="/" className='text-decoration-none brand-name'>
      <span>Aves</span>
      <span>LOG</span>
    </Link>
  </div>
);
