import React from 'react';
import { withTranslation } from 'react-i18next';
import { Route } from "react-router-dom";
import CreatePasswordReset from './CreatePasswordReset.js';

function PasswordReset({ match }) {

  const renderCreatePasswordReset = props => {
    return <CreatePasswordReset {...props}/>
  };

  const renderPasswordResetForm = props => {
    return <div>{props.match.params.token}</div>;
  };

  return (
    <div>
      <Route exact path={match.path} render={renderCreatePasswordReset}/>
      <Route path={`${match.path}/:token`} render={renderPasswordResetForm}/>
    </div>
  );
}

export default withTranslation()(PasswordReset);
