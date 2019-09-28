import React from 'react';
import { Route } from "react-router-dom";
import Settings from './settings/settings'
import Home from './home/Home.js';
import Authentication from './authentication/Authentication.js'
import Bird from './bird/Bird.js';
import Sighting from './sighting/Sighting.js';

export default () => {
  return (
    <main role="main">
      <Route path='/' exact component={Home} />
      <Route path='/authentication' component={Authentication} />
      <Route path='/settings' exact component={Settings} />
      <Route path='/bird' component={Bird} />
      <Route path='/sighting' component={Sighting} />
    </main>
  );
}
