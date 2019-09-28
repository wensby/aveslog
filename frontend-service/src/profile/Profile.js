import React from 'react';
import { Switch, Route } from "react-router-dom";
import ProfilePage from './ProfilePage.js';

export default ({ match }) => {
  const renderProfilePage = props => {
    return <ProfilePage username={props.match.params.username}/>;
  }

  return <Switch>
    <Route path={`${match.path}/:username`} render={renderProfilePage} />
  </Switch>;
}
