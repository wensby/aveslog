import React from 'react';
import { Switch, Route } from 'react-router-dom';
import SightingsPage from './SightingsPage';
import { SightingPage } from './SightingPage.js';
import AuthenticatedRoute from '../authentication/AuthenticatedRoute.js';

export default ({match}) => {
  const { path } = match;
  return (
    <Switch>
      <AuthenticatedRoute exact path={`${path}`} component={SightingsPage} />
      <Route path={`${path}/:sightingId`} component={SightingPage} />
    </Switch>
  );
}
