import React from 'react';
import { Switch, Route } from "react-router-dom";
import PasswordReset from './PasswordReset.js';
import Login from './Login.js';
import RegisterEmail from './RegisterEmail.js';

export default ({ match }) => {
  return (
    <Switch>
      <Route path={`${match.path}/login`} component={Login}/>
      <Route path={`${match.path}/register`} component={RegisterEmail}/>
      <Route path={`${match.path}/password-reset`} component={PasswordReset}/>
    </Switch>
  );
}
