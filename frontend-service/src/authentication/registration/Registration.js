import React from 'react';
import { Switch, Route } from "react-router-dom";
import { EmailRegistrationPage } from './EmailRegistrationPage';
import { CredentialsRegistrationPage } from './CredentialsRegistrationPage';

export const Registration = ({ match }) => {
  const path = match.path;
  return (
    <Switch>
      <Route exact path={`${path}`} component={EmailRegistrationPage} />
      <Route path={`${path}/:token`} component={CredentialsRegistrationPage} />
    </Switch>
  );
};
