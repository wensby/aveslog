import React from 'react';
import { Route } from "react-router-dom";
import Settings from './settings/SettingsRoute'
import HomePage from './home/HomePage';
import Authentication from './authentication/Authentication.js'
import Bird from './bird/Bird.js';
import Sighting from './sighting/Sighting.js';
import { Profile } from './profile/Profile';
import AuthenticatedRoute from './authentication/AuthenticatedRoute';
import { Birder } from './birder/Birder';
import './Main.scss';

export const Main = () => {
  return (
    <div className='main'>
      <main role='main'>
        <Route path='/' exact component={HomePage} />
        <Route path='/authentication' component={Authentication} />
        <Route path='/profile' component={Profile} />
        <Route path='/birder' component={Birder} />
        <AuthenticatedRoute path='/settings' exact component={Settings} />
        <Route path='/bird' component={Bird} />
        <Route path='/sighting' component={Sighting} />
      </main>
    </div>
  );
};
