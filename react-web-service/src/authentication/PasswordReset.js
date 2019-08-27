import React from 'react';
import { withTranslation } from 'react-i18next';
import { Route } from "react-router-dom";
import CreatePasswordReset from './CreatePasswordReset.js';
import PasswordResetForm from './PasswordResetForm.js';

function PasswordReset({ match }) {

  const renderCreatePasswordReset = props => {
    return <CreatePasswordReset {...props}/>
  };

  const renderPasswordResetForm = props => {
    return <PasswordResetForm {...props} />;
  };

  return (
    <div>
      <Route exact path={match.path} render={renderCreatePasswordReset}/>
      <Route path={`${match.path}/:token`} render={renderPasswordResetForm}/>
    </div>
  );
}

export default withTranslation()(PasswordReset);
