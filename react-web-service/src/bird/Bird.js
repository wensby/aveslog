import React from 'react';
import { Switch, Route } from "react-router-dom";
import BirdQueryResult from './BirdQueryResult';
import BirdDetails from './BirdDetails.js';
import NewBirdSighting from './NewBirdSighting';

export default function Bird({ match }) {
  return (
    <Switch>
      <Route path={`${match.path}/search`} component={BirdQueryResult}/>
      <Route path={`${match.path}/:binomialName`} exact component={BirdDetails}/>
      <Route path={`${match.path}/:binomialName/new-sighting`} exact component={NewBirdSighting} />
    </Switch>
  );
}
