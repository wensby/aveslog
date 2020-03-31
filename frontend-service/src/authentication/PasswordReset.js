import React from 'react';
import { Route, Switch } from "react-router-dom";
import { CreatePasswordReset } from './CreatePasswordReset.js';
import { PasswordResetForm } from './PasswordResetForm.js';

export const PasswordReset = ({ match }) => {
  const { path } = match;

  return (
    <Switch>
      <Route exact path={path} component={CreatePasswordReset}/>
      <Route path={`${path}/:token`} component={PasswordResetForm}/>
    </Switch>
  );
};
