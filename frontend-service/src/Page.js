import React from 'react';
import { Navbar } from './navbar/Navbar.js';
import { Sidebar } from './Sidebar.js';
import { Main } from './Main.js';
import { Footer } from './footer/Footer.js';
import './Page.scss';

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
