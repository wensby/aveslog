import React, { useState, useEffect, useContext } from 'react';
import { Link } from "react-router-dom";
import Button from 'react-bootstrap/Button';
import { Navbar as BootstrapNavbar } from "react-bootstrap";
import './navbar.css';
import Menu from './Menu.js';
import SearchBar from './SearchBar';
import { AuthenticationContext } from '../authentication/AuthenticationContext.js';
import { getMenuItems } from './MenuItemsFactory.js';
import { useTranslation } from 'react-i18next';

function Brand() {
  return (
    <BootstrapNavbar.Brand>
      <Link to="/">
        <img id='navbarLogoImage' src='/birdlogo-50.png' alt=''/>
      </Link>
    </BootstrapNavbar.Brand>
  );
}

export default () => {
  const [menuCollapseState, setMenuCollapseState] = useState('collapsed');
  const {authenticated, account, unauthenticate} = useContext(AuthenticationContext);
  const { t } = useTranslation();
  let fullNavbarRef = null;
  let gridRef = null;

  useEffect(() => {
    document.addEventListener('click', onDocumentClick, true);
    return () => document.removeEventListener('click', onDocumentClick);
  }, []);

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

  const collapseMenu = () => {
    setMenuCollapseState('collapsing');
  }

  const isMenuFullyCollapsed = () => {
    return menuCollapseState === 'collapsed';
  }

  const isTargetOutsideNavbar = target => {
    return fullNavbarRef && !fullNavbarRef.contains(target);
  }

  const isTargetInsideStaticNavbar = target => {
    return gridRef && gridRef.contains(target);
  }

  const onDocumentClick = event => {
    if (!isMenuFullyCollapsed()) {
      const target = event.target;
      if (isTargetOutsideNavbar(target)) {
        collapseMenu();
        event.preventDefault();
      }
      else if (isTargetInsideStaticNavbar(target)) {
        collapseMenu();
      }
    }
  };

  const renderMainArea = () => {
    return (
      <div className='navbar-main d-flex mr-0 flex-grow-1 align-self-center'>
        <div className='flex-grow-1 align-self-center'>
          <Brand />
          {renderUsername()}
        </div>
      </div>
    );
  }

  const renderUsername = () => {
    if (authenticated && account) {
      return (
        <Link className='text-light' to={`/profile/${account.username}`}>
          {account.username}
        </Link>
      );
    }
  }

  const renderMenuButton = () => {
    return (
      <div className='menu-button'>
        <Button onClick={toggleNavbar} className='navbar-toggler'>
          <span className="navbar-toggler-icon"></span>
        </Button>
      </div>
    );
  }

  const renderSearch = () => {
    return (
      <div className='search-bar-item'>
        <SearchBar />
      </div>
    );
  }

  
  const items = getMenuItems(authenticated, account, unauthenticate, t);
  const needMaxHeight = ['expanding', 'expanded'].indexOf(menuCollapseState) >= 0; 
  const style = needMaxHeight ? {maxHeight: `${items.length * 37}px`} : {};

  return (
    <div ref={setFullNavbarRef}
      className="navbar navbar-dark shadow p-0 bg-primary fixed-top">
      <div ref={setGridRef} className='grid'>
        {renderMainArea()}
        {renderMenuButton()}
        {renderSearch()}
      </div>
      <div className={`menu ${menuCollapseState}`} style={style}>
        <Menu items={items} onClick={() => setTimeout(collapseMenu, 0)} />
      </div>
    </div>
  );
}
