import React, { useContext } from 'react';
import { NavbarContext } from './Navbar.js';
import { useMenuItems } from '../useMenuItems.js';
import { Link } from 'react-router-dom';
import './ExpandibleMenu.scss';

export const ExpandibleMenu = ({ state }) => {
  const { collapseMenu } = useContext(NavbarContext);
  const items = useMenuItems();
  const needMaxHeight = ['expanding', 'expanded'].indexOf(state) >= 0;
  const style = needMaxHeight ? { maxHeight: `${items.length * 37}px` } : {};

  return (
    <div className={`expandible-menu ${state}`} style={style}>
      <div className='navbar-nav' id='collapsableMenuList' onClick={collapseMenu}>
        {items.map((item, index) => <MenuItem key={index} item={item} />)}
      </div>
    </div>
  );
};

const MenuItem = ({ item }) => {
  if (item.link) {
    return <Link className='nav-link' to={item.link} onClick={item.action}>{item.label}</Link>;
  }
  else {
    return <div className='nav-link' onClick={item.action}>{item.label}</div>
  }
};
