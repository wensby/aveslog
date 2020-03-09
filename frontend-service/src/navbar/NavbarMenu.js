import React, { useContext } from 'react';
import { NavbarContext } from './Navbar.js';
import { useMenuItems } from '../useMenuItems.js';
import { MenuItem } from '../menu/MenuItem.js';
import './NavbarMenu.scss';

export const NavbarMenu = ({ state }) => {
  const { collapseMenu } = useContext(NavbarContext);
  const items = useMenuItems();
  const needMaxHeight = ['expanding', 'expanded'].indexOf(state) >= 0;
  const style = needMaxHeight ? { maxHeight: `${items.length * 37}px` } : null;
  const classNames = ['navbar-menu', state];

  return (
    <nav className={classNames.join(' ')} style={style} onClick={collapseMenu}>
      {items.map((item, index) => <MenuItem key={index} item={item} />)}
    </nav>
  );
};
