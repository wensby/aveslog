import React, { useState, useEffect } from 'react';
import './style.scss';
import { ExpandibleMenu } from './ExpandibleMenu';
import { NavbarConstant } from './NavbarConstant';

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

  return (
    <div ref={setFullNavbarRef} className="navbar navbar-light shadow p-0 fixed-top">
      <NavbarConstant ref={setGridRef} onToggleNavbarClick={toggleNavbar} />
      <ExpandibleMenu collapseState={menuCollapseState} onMenuClick={() => setTimeout(collapseMenu, 0)} />
    </div>
  );
}
