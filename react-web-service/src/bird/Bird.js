import React from 'react';
import { Route } from "react-router-dom";
import BirdQueryResult from './BirdQueryResult';

export default function Bird({ match }) {
  return (
    <div>
      <Route path={`${match.path}/search`} component={BirdQueryResult}/>
    </div>
  );
}
