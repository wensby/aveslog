import React from 'react';
import { Switch } from "react-router-dom";
import { AuthenticatedRoute } from '../authentication/AuthenticatedRoute';
import { BirdersPage } from 'pages';
import { BirderPageContainer } from '../birder/BirderPageContainer.js';

export const BirdersRoute = ({ match }) => {
  const { path } = match;

  const renderBirderPage = props => {
    return <BirderPageContainer birderId={props.match.params.birderId}/>;
  };

  return (
    <Switch>
      <AuthenticatedRoute exact path={path} component={BirdersPage} />
      <AuthenticatedRoute path={`${path}/:birderId`} render={renderBirderPage} />
    </Switch>
  );
};
