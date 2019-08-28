import React from 'react';
import { Switch, Route } from 'react-router-dom';
import SightingList from './SightingList.js';
import SightingDetails from './SightingDetails.js';

export default function Sighting({ match }) {
  return (
    <Switch>
      <Route exact path={`${match.path}`} component={SightingList} />
      <Route path={`${match.path}/:sightingId`} component={SightingDetails} />
    </Switch>
  );
}
