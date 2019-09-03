import React, { useContext } from 'react';
import { AuthenticationContext } from './authentication/AuthenticationContext.js';
import { getMenuItems } from './navbar/MenuItemsFactory.js';
import { useTranslation } from 'react-i18next';

export default () => {
  const { t } = useTranslation();
  const { authenticated, account, unauthenticate } = useContext(AuthenticationContext);
  const items = getMenuItems(authenticated, account, unauthenticate, t);

  const renderItem = (item, index) => {
    return <div className="nav-item" key={index}>{item}</div>;
  };

  return (
    <div className="sidemenu">
      <nav className="sidebar nav flex-column border-left" id="sidebarList">
        {items.map(renderItem)}
      </nav>
    </div>
  );
}
