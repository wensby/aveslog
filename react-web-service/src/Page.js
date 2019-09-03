import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React from 'react';
import Navbar from './navbar/navbar.js';
import SideMenu from './Side_Menu.js';
import './App.css';
import Main from './Main.js';

export default () => {
  return (
    <>
      <Navbar />
      <div className='main-grid navbar-pushed'>
        <SideMenu />
        <Main />
      </div>
    </>
  );
}
