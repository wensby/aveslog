import React from 'react';
import { Switch, Route } from "react-router-dom";
import PasswordReset from './PasswordReset.js';
import { Login } from './Login.js';
import Registration from './registration/Registration.js';

export default ({ match }) => {
  const { path } = match;
  return (
    <Switch>
      <Route path={`${path}/login`} component={Login}/>
      <Route path={`${path}/registration`} component={Registration}/>
      <Route path={`${path}/password-reset`} component={PasswordReset}/>
    </Switch>
  );
}
