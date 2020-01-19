import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import './style.scss';
import { SearchBar } from './SearchBar';
import { NavbarMain } from './NavbarMain';
import { ExpandibleMenu } from './ExpandibleMenu';

export function Navbar() {
  const [menuCollapseState, setMenuCollapseState] = useState('collapsed');
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

  const renderStaticPart = () =>
    <div ref={setGridRef} className='navbar-grid'>
      <NavbarMain />
      <div className='menu-button'>
        <Button onClick={toggleNavbar} className='navbar-toggler'>
          <span className="navbar-toggler-icon"></span>
        </Button>
      </div>
      <div className='search-bar-item'>
        <SearchBar />
      </div>
    </div>;

  return (
    <div ref={setFullNavbarRef}
      className="navbar navbar-light shadow p-0 fixed-top">
      {renderStaticPart()}
      <ExpandibleMenu menuCollapseState={menuCollapseState} onMenuClick={() => setTimeout(collapseMenu, 0)} />
    </div>
  );
}
