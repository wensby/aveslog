import React from 'react';
import { NavbarBrand } from './NavbarBrand';
import { NavbarUsername } from './NavbarUsername';
import { useAuthentication } from '../authentication/AuthenticationHooks';
import './NavbarMain.scss';

export function NavbarMain() {
  const { account } = useAuthentication();

  return (
    <div className='navbar-main'>
      <NavbarBrand />
      {account && <NavbarUsername username={account.username} />}
    </div>
  );
}
