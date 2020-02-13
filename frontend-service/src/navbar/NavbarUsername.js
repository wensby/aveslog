import React from 'react';
import { Link } from 'react-router-dom';
import './NavbarUsername.scss';

export const NavbarUsername = ({username}) => (
  <div className='navbar-username'>
    <Link to={`/profile/${username}`}>{username}</Link>
  </div>
);
