import React from 'react';
import { Switch, Route } from "react-router-dom";
import PasswordReset from './PasswordReset.js';
import { Login } from './LoginPage.js';
import Registration from './registration/Registration.js';

export const Authentication = ({ match }) => {
  const { path } = match;
  return (
    <Switch>
      <Route path={`${path}/login`} component={Login} />
      <Route path={`${path}/registration`} component={Registration} />
      <Route path={`${path}/password-reset`} component={PasswordReset} />
    </Switch>
  );
};
