import React from 'react';
import { Route } from "react-router-dom";
import { Settings } from './settings/SettingsRoute'
import { HomePage } from './home/HomePage';
import { Authentication } from './authentication/Authentication.js'
import { BirdRoute } from './bird/BirdRoute.js';
import { Sighting } from './sighting/Sighting.js';
import { BirdersRoute } from './profile/BirdersRoute';
import AuthenticatedRoute from './authentication/AuthenticatedRoute';
import './Main.scss';

export const Main = () => {
  return (
    <main role='main'>
      <Route path='/' exact component={HomePage} />
      <Route path='/authentication' component={Authentication} />
      <Route path='/birders' component={BirdersRoute} />
      <AuthenticatedRoute path='/settings' exact component={Settings} />
      <Route path='/bird' component={BirdRoute} />
      <Route path='/sighting' component={Sighting} />
    </main>
  );
};
