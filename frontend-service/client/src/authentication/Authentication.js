import React from 'react';
import { Switch, Route } from "react-router-dom";
import { LoginPage } from 'pages';
import { Registration } from './registration/Registration.js';
import { CreatePasswordReset } from './CreatePasswordReset.js';
import { PasswordResetForm } from './PasswordResetForm.js';

export const Authentication = ({ match }) => {
  const { path } = match;
  return (
    <Switch>
      <Route path={`${path}/login`} component={LoginPage} />
      <Route path={`${path}/registration`} component={Registration} />
      <Route path={`${path}/credentials-recovery`} component={CreatePasswordReset}/>
      <Route path={`${path}/password-reset/:token`} component={PasswordResetForm}/>
    </Switch>
  );
};
