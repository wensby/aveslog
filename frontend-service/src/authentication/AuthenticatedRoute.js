import React, { useContext } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { UserContext } from './UserContext.js';

export default ({ component, ...routeProps }) => {
  const { authenticated } = useContext(UserContext);
  const path = '/authentication/login';

  if (authenticated) {
    return <Route {...routeProps} component={component} />;
  }
  else {
    return <Route {...routeProps} render={() => <Redirect to={path} />} />;
  }
};
