import React, { useContext } from 'react';
import { NavbarBrand } from './NavbarBrand';
import { NavbarUsername } from './NavbarUsername';
import { UserContext } from '../authentication/UserContext.js';

export function NavbarMain() {
  const { authenticated, account } = useContext(UserContext);

  return (
    <div className='navbar-main'>
      <NavbarBrand />
      {authenticated && <NavbarUsername username={account.username} />}
    </div>
  );
}
