import React from 'react';
import { Switch, Route } from 'react-router-dom';
import { BirdSearchResultsPage } from 'pages';
import { RoutedBirdPage } from 'pages';
import { NewBirdSighting } from '../sighting/NewBirdSighting';

export const BirdRoute = ({ match }) => {
  const { path } = match;

  return (
    <Switch>
      <Route path={`${path}/search`} component={BirdSearchResultsPage} />
      <Route path={`${path}/:birdId`} exact component={RoutedBirdPage} />
      <Route
        path={`${path}/:birdId/new-sighting`}
        exact
        component={NewBirdSighting} />
    </Switch>
  );
}
