import React from 'react';
import { Route } from "react-router-dom";
import queryString from 'query-string';

function BirdQuery({ location }) {
  const query = queryString.parse(location.search);
  console.log(query);
  return <h1>{`Bird - ${query.q}`}</h1>;
}

export default function Bird({ match }) {
  return (
    <div>
      <Route path={`${match.path}/search`} component={BirdQuery}/>
    </div>
  );
}
