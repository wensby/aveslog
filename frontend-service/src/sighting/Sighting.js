import React from 'react';
import { Switch, Route } from 'react-router-dom';
import SightingListContainer from './SightingListContainer.js';
import SightingDetails from './SightingDetails.js';
import AuthenticatedRoute from '../authentication/AuthenticatedRoute.js';

export default ({match}) => {
  const { path } = match;
  return (
    <Switch>
      <AuthenticatedRoute exact path={`${path}`} component={SightingListContainer} />
      <Route path={`${match.path}/:sightingId`} component={SightingDetails} />
    </Switch>
  );
}
