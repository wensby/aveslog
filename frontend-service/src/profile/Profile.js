import React from 'react';
import { Switch } from "react-router-dom";
import ProfilePage from './ProfilePage.js';
import AuthenticatedRoute from '../authentication/AuthenticatedRoute';

export default ({ match }) => {
  const renderProfilePage = props => {
    return <ProfilePage username={props.match.params.username}/>;
  }

  return (
    <Switch>
      <AuthenticatedRoute path={`${match.path}/:username`} render={renderProfilePage} />
    </Switch>
  );
}
