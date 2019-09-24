import React, { useState, useEffect, useContext } from 'react';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import { Navbar as BootstrapNavbar } from "react-bootstrap";
import './navbar.scss';
import Menu from './Menu.js';
import SearchBar from './SearchBar';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';
import { getMenuItems } from './MenuItemsFactory.js';
import { useTranslation } from 'react-i18next';

function Brand() {
  return (
    <BootstrapNavbar.Brand>
      <Link to="/" className='text-decoration-none brand-name'>
        Aves Log
      </Link>
    </BootstrapNavbar.Brand>
  );
}

export default () => {
  const [menuCollapseState, setMenuCollapseState] = useState('collapsed');
  const { authenticated, account, unauthenticate } = useContext(AuthenticationContext);
  const { t } = useTranslation();
  let fullNavbarRef = null;
  let gridRef = null;

  const isNavbarShowing = () => {
    return menuCollapseState !== 'collapsed';
  }

  const onDocumentClick = event => {
    if (isNavbarShowing()) {
      if (isTargetOutsideNavbar(event.target)) {
        collapseMenu();
        event.preventDefault();
      }
      else if (isTargetInsideStaticPartOfNavbar(event.target)) {
        collapseMenu();
      }
    }
  };

  const collapseMenu = () => {
    setMenuCollapseState('collapsing');
  }

  useEffect(() => {
    document.addEventListener('click', onDocumentClick, true);
    return () => document.removeEventListener('click', onDocumentClick);
  });

  useEffect(() => {
    if (menuCollapseState === 'expanding') {
      setTimeout(() => {
        if (menuCollapseState === 'expanding') {
          setMenuCollapseState('expanded');
        }
      }, 300);
    }
    else if (menuCollapseState === 'collapsing') {
      setTimeout(() => {
        if (menuCollapseState === 'collapsing') {
          setMenuCollapseState('collapsed');
        }
      }, 300);
    }
  }, [menuCollapseState])

  const setFullNavbarRef = node => {
    fullNavbarRef = node;
  }

  const setGridRef = node => {
    gridRef = node;
  }

  const toggleNavbar = () => {
    if (menuCollapseState === 'collapsed') {
      setMenuCollapseState('expanding');
    }
    if (menuCollapseState === 'expanded') {
      collapseMenu();
    }
  };

  const isTargetOutsideNavbar = target => {
    return fullNavbarRef && !fullNavbarRef.contains(target);
  }

  const isTargetInsideStaticPartOfNavbar = target => {
    return gridRef && gridRef.contains(target);
  }

  const renderUsername = () => {
    if (authenticated && account) {
      return (
        <Link className='text-dark' to={`/profile/${account.username}`}>
          {account.username}
        </Link>
      );
    }
  }

  const renderStaticPart = () =>
    <div ref={setGridRef} className='grid'>
      <div className='navbar-main d-flex mr-0 flex-grow-1 align-self-center'>
        <div className='flex-grow-1 align-self-center'>
          <Brand />
          {renderUsername()}
        </div>
      </div>
      <div className='menu-button'>
        <Button onClick={toggleNavbar} className='navbar-toggler'>
          <span className="navbar-toggler-icon"></span>
        </Button>
      </div>
      <div className='search-bar-item'>
        <SearchBar />
      </div>
    </div>;

  const renderExpandibleMenu = () => {
    const items = getMenuItems(authenticated, account, unauthenticate, t);
    const needMaxHeight = ['expanding', 'expanded'].indexOf(menuCollapseState) >= 0;
    const style = needMaxHeight ? { maxHeight: `${items.length * 37}px` } : {};
    return (
      <div className={`menu ${menuCollapseState}`} style={style}>
        <Menu items={items} onClick={() => setTimeout(collapseMenu, 0)} />
      </div>
    );
  }

  return (
    <div ref={setFullNavbarRef}
      className="navbar navbar-light shadow p-0 fixed-top">
      {renderStaticPart()}
      {renderExpandibleMenu()}
    </div>
  );
}
