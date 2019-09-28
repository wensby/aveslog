import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React from 'react';
import TopNavbar from './navbar/TopNavbar.js';
import SideMenu from './SideMenu.js';
import './App.css';
import Main from './Main.js';
import Footer from './Footer.js';
import './style.scss';

export default () => {
  return (
    <div className='page-container'>
      <TopNavbar />
      <div className='main-grid navbar-pushed'>
        <SideMenu />
        <Main />
      </div>
      <Footer />
    </div>
  );
}
