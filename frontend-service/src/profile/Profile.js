import React from 'react';
import { Switch } from "react-router-dom";
import { ProfilePage } from './ProfilePage.js';
import AuthenticatedRoute from '../authentication/AuthenticatedRoute';
import { ProfilesPage } from './ProfilesPage';

export function Profile({ match }) {
  const { path } = match;

  const renderProfilePage = props => {
    return <ProfilePage username={props.match.params.username}/>;
  }

  return (
    <Switch>
      <AuthenticatedRoute exact path={path} component={ProfilesPage} />
      <AuthenticatedRoute path={`${path}/:username`} render={renderProfilePage} />
    </Switch>
  );
}
