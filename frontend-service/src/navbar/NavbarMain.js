import React from 'react';
import { NavbarBrand } from './NavbarBrand';
import { NavbarAccount } from './NavbarAccount';
import { useAuthentication } from '../authentication/AuthenticationHooks';
import './NavbarMain.scss';

export function NavbarMain() {
  const { account } = useAuthentication();

  return (
    <div className='navbar-main'>
      <NavbarBrand />
      {account && <NavbarAccount account={account} />}
    </div>
  );
}
