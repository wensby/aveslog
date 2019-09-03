import React from 'react';
import { Switch, Route } from "react-router-dom";
import RegisterEmail from './RegisterEmail';
import RegistrationForm from './RegistrationForm.js';

export default ({ match }) => {
  return (
    <Switch>
      <Route exact path={`${match.path}`} component={RegisterEmail} />
      <Route path={`${match.path}/:token`} component={RegistrationForm} />
    </Switch>
  );
}
