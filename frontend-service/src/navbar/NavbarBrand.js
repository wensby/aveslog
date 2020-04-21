import React, { useContext } from 'react';
import { Link } from "react-router-dom";
import { Brand } from 'specific/Brand.js';
import './NavbarBrand.scss';
import { HomeContext } from 'specific/HomeContext';

export const NavbarBrand = () => {
  const { incrementHomeTrigger } = useContext(HomeContext);

  const handleClick = () => {
    incrementHomeTrigger();
  };

  return <div className='navbar-brand'>
    <Link onClick={handleClick} to='/home' className='text-decoration-none'>
      <Brand />
    </Link>
  </div>
};
