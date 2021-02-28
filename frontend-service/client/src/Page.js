import React from 'react';
import { Switch } from 'react-router';
import { Route } from 'react-router-dom';
import { SplashPage } from 'splash/SplashPage.js';
import { Navbar } from './navbar/Navbar.js';
import { Main } from './Main.js';
import { Footer } from './footer/Footer.js';
import './Page.scss';

export const Page = () => {
  return (
    <Switch>
      <Route path='/' exact>
        <SplashPage />
      </Route>
      <Route>
        <Navbar />
        <Main />
        <Footer />
      </Route>
    </Switch>
  );
};
