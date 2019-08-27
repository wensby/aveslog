import React from 'react';
import { Switch, Route } from "react-router-dom";
import BirdQueryResult from './BirdQueryResult';
import BirdDetails from './BirdDetails.js';

export default function Bird({ match }) {
  return (
    <Switch>
      <Route path={`${match.path}/search`} component={BirdQueryResult}/>
      <Route path={`${match.path}/:binomialName`} component={BirdDetails}/>
    </Switch>
  );
}
