import 'bootstrap/dist/css/bootstrap.css';

import React from 'react';
import Navbar from './navbar/Navbar.js';
import SideMenu from './SideMenu.js';
import Main from './Main.js';
import Footer from './Footer.js';
import './style.scss';

const Between = () => (
  <div className='between'>
    <SideMenu />
    <Main />
  </div>
);

export default () => {
  return (
    <>
      <Navbar />
      <Between />
      <Footer />
    </>
  );
}
