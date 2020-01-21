import React from 'react';
import { Switch, Route } from "react-router-dom";
import { BirdSearchResultsPage } from './BirdSearchResultsPage';
import { BirdPage } from './BirdPage.js';
import { NewBirdSighting } from '../sighting/NewBirdSighting';

export default function Bird({ match }) {
  const { path } = match;
  return (
    <Switch>
      <Route path={`${path}/search`} component={BirdSearchResultsPage}/>
      <Route path={`${path}/:binomialName`} exact component={BirdPage}/>
      <Route path={`${path}/:binomialName/new-sighting`} exact component={NewBirdSighting} />
    </Switch>
  );
}
