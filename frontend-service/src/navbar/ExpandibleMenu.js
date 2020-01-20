import React, { useContext } from 'react';
import { Menu } from './Menu.js';
import { UserContext } from '../authentication/UserContext.js';
import { getMenuItems } from './MenuItemsFactory.js';
import { useTranslation } from 'react-i18next';

export function ExpandibleMenu({ state, onItemClick }) {
  const { authenticated, account, unauthenticate } = useContext(UserContext);
  const { t } = useTranslation();
  const items = getMenuItems(authenticated, account, unauthenticate, t);
  const needMaxHeight = ['expanding', 'expanded'].indexOf(state) >= 0;
  const style = needMaxHeight ? { maxHeight: `${items.length * 37}px` } : {};

  return (
    <div className={`menu ${state}`} style={style}>
      <Menu items={items} onClick={onItemClick} />
    </div>
  );
}
