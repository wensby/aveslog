import React from 'react';
import { Navbar } from './navbar/Navbar.js';
import Sidebar from './SideMenu.js';
import Main from './Main.js';
import Footer from './Footer.js';
import './style.scss';

export const Page = () => {
  return (
    <>
      <Navbar />
      <Sidebar />
      <Main />
      <Footer />
    </>
  );
};
