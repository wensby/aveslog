import React, { useContext } from 'react';
import { Link } from "react-router-dom";
import { UserContext } from '../authentication/UserContext.js';

export function NavbarUsername() {
  const { authenticated, account } = useContext(UserContext);
  if (authenticated && account) {
    return (
      <div className='navbar-username'>
        <Link to={`/profile/${account.username}`}>{account.username}</Link>
      </div>
    );
  }
  else {
    return null;
  }
}
