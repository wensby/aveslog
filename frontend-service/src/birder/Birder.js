import React, { useState, useEffect } from 'react';
import { Switch } from 'react-router-dom';
import AuthenticatedRoute from '../authentication/AuthenticatedRoute';
import BirderPage from './BirderPage';
import Spinner from '../loading/Spinner';
import { useBirder } from '../birder/BirderHooks';


export default function Birder({ match }) {
  const { path } = match;
  return (
    <Switch>
      <AuthenticatedRoute
        path={`${path}/:birderId`}
        render={props => <BirderPageContiner birderId={props.match.params.birderId}/>} />
    </Switch>
  );
}

function BirderPageContiner({ birderId }) {
  const birder = useBirder(birderId);

  if (!birder) {
    return <div><Spinner /></div>;
  }
  return <BirderPage birder={birder} />
}
