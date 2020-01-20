import React from 'react';
import { Link } from "react-router-dom";

export const NavbarUsername = ({username}) => (
  <div className='navbar-username'>
    <Link to={`/profile/${username}`}>{username}</Link>
  </div>
);
