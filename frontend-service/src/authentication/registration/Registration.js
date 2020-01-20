import React from 'react';
import { Switch, Route } from "react-router-dom";
import EmailRegistration from './EmailRegistration';
import { CredentialsRegistrationPage } from './CredentialsRegistrationPage';

export default ({ match }) => {
  const path = match.path;
  return (
    <Switch>
      <Route exact path={`${path}`} component={EmailRegistration} />
      <Route path={`${path}/:token`} component={CredentialsRegistrationPage} />
    </Switch>
  );
}
