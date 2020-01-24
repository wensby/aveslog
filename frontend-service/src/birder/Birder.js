import React from 'react';
import { Switch } from 'react-router-dom';
import AuthenticatedRoute from '../authentication/AuthenticatedRoute';
import { BirderPageContainer } from './BirderPageContainer';

export function Birder({ match }) {
  const { path } = match;
  return (
    <Switch>
      <AuthenticatedRoute
        path={`${path}/:birderId`}
        render={props => <BirderPageContainer birderId={props.match.params.birderId}/>} />
    </Switch>
  );
}
