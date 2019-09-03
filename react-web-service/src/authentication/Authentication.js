import React from 'react';
import { Switch, Route } from "react-router-dom";
import PasswordReset from './PasswordReset.js';
import Login from './Login.js';
import Registration from './Registration.js';

export default ({ match }) => {
  return (
    <Switch>
      <Route path={`${match.path}/login`} component={Login}/>
      <Route path={`${match.path}/registration`} component={Registration}/>
      <Route path={`${match.path}/password-reset`} component={PasswordReset}/>
    </Switch>
  );
}
