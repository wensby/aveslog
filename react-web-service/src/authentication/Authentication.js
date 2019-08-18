import React from 'react';
import { withTranslation } from 'react-i18next';
import { Route } from "react-router-dom";
import PasswordReset from './PasswordReset.js';
import Login from './Login.js';
import Register from './Register.js';

function Authentication({ match }) {

  const renderLogin = props => {
    return <Login {...props} />;
  };

  const renderRegistration = props => {
    return <Register {...props} />;
  };

  const renderPasswordReset = props => {
    return <PasswordReset {...props} />;
  };

  const path = match.path;
  return (
    <div>
      <Route path={`${path}/login`} render={renderLogin}/>
      <Route path={`${path}/register`} render={renderRegistration}/>
      <Route path={`${path}/password-reset`} render={renderPasswordReset}/>
    </div>
  );
}

export default withTranslation()(Authentication);
