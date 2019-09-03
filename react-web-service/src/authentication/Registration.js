import React from 'react';
import { Switch, Route } from "react-router-dom";
import RegisterEmail from './RegisterEmail';

export default ({ match }) => {
  return (
    <Switch>
      <Route exact path={`${match.path}`} component={RegisterEmail} />
    </Switch>
  );
}
