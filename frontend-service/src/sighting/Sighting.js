import React from 'react';
import { Switch, Route } from 'react-router-dom';
import { SightingsPage } from 'pages';
import { SightingPage } from 'pages';
import { AuthenticatedRoute } from '../authentication/AuthenticatedRoute.js';

export const Sighting = ({ match }) => {
  const { path } = match;
  return (
    <Switch>
      <AuthenticatedRoute exact path={`${path}`} component={SightingsPage} />
      <Route path={`${path}/:sightingId`} component={SightingPage} />
    </Switch>
  );
};
