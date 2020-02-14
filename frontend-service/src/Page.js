import React from 'react';
import { Navbar } from './navbar/Navbar.js';
import { SideMenu } from './SideMenu.js';
import Main from './Main.js';
import { Footer } from './footer/Footer.js';
import './style.scss';

export const Page = () => {
  return (
    <>
      <Navbar />
      <SideMenu />
      <Main />
      <Footer />
    </>
  );
};
