import React, { useContext } from 'react';
import { Menu } from './Menu.js';
import { UserContext } from '../authentication/UserContext.js';
import { getMenuItems } from './MenuItemsFactory.js';
import { useTranslation } from 'react-i18next';

export function ExpandibleMenu({ collapseState, onMenuClick }) {
  const { authenticated, account, unauthenticate } = useContext(UserContext);
  const { t } = useTranslation();
  const items = getMenuItems(authenticated, account, unauthenticate, t);
  const needMaxHeight = ['expanding', 'expanded'].indexOf(collapseState) >= 0;
  const style = needMaxHeight ? { maxHeight: `${items.length * 37}px` } : {};
  return (<div className={`menu ${collapseState}`} style={style}>
    <Menu items={items} onClick={onMenuClick} />
  </div>);
}
