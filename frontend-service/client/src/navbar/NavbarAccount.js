import React from 'react';
import { Link } from 'react-router-dom';
import './NavbarAccount.scss';

export const NavbarAccount = ({ account }) => (
  <div className='navbar-account'>
    <Link to={`/birders/${account.birder.id}`}>{account.birder.name}</Link>
  </div>
);
