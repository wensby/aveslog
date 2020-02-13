import React, { useContext } from 'react';
import { Menu } from './Menu.js';
import { NavbarContext } from './Navbar.js';
import './ExpandibleMenu.scss';
import { useMenuItems } from '../useMenuItems.js';

export const ExpandibleMenu = ({ state }) => {
  const { collapseMenu } = useContext(NavbarContext);
  const items = useMenuItems();
  const needMaxHeight = ['expanding', 'expanded'].indexOf(state) >= 0;
  const style = needMaxHeight ? { maxHeight: `${items.length * 37}px` } : {};

  return (
    <div className={`expandible-menu ${state}`} style={style}>
      <Menu items={items} onClick={collapseMenu} />
    </div>
  );
}
