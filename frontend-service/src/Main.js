import React from 'react';
import { Route } from "react-router-dom";
import Settings from './settings/settings'
import Home from './home/Home.js';
import Authentication from './authentication/Authentication.js'
import Bird from './bird/Bird.js';
import Sighting from './sighting/Sighting.js';
import Profile from './profile/Profile';
import AuthenticatedRoute from './authentication/AuthenticatedRoute';

export default () => {
  return (
    <div className='main-grid'>
      <main role="main">
        <Route path='/' exact component={Home} />
        <Route path='/authentication' component={Authentication} />
        <Route path='/profile' component={Profile} />
        <AuthenticatedRoute path='/settings' exact component={Settings} />
        <Route path='/bird' component={Bird} />
        <Route path='/sighting' component={Sighting} />
      </main>
    </div>
  );
}
