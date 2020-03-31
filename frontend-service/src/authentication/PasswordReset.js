import React from 'react';
import { Route, Switch } from "react-router-dom";
import { CreatePasswordReset } from './CreatePasswordReset.js';
import { PasswordResetForm } from './PasswordResetForm.js';

export const PasswordReset = ({ match }) => {
  const { path } = match;

  const renderCreatePasswordReset = props => {
    return <CreatePasswordReset {...props}/>
  };

  const renderPasswordResetForm = props => {
    return <PasswordResetForm {...props} />;
  };

  return (
    <Switch>
      <Route exact path={path} render={renderCreatePasswordReset}/>
      <Route path={`${path}/:token`} render={renderPasswordResetForm}/>
    </Switch>
  );
};
