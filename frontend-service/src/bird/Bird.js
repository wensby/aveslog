import React from 'react';
import { Switch, Route } from "react-router-dom";
import BirdQueryResult from './BirdQueryResult';
import BirdDetails from './BirdDetails.js';
import NewBirdSighting from './NewBirdSighting';

export default function Bird({ match }) {
  const { path } = match;
  return (
    <Switch>
      <Route path={`${path}/search`} component={BirdQueryResult}/>
      <Route path={`${path}/:binomialName`} exact component={BirdDetails}/>
      <Route path={`${path}/:binomialName/new-sighting`} exact component={NewBirdSighting} />
    </Switch>
  );
}
