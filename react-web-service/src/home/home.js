import React from 'react';

export default function Home(props) {
  if (props.authenticated) {
    return (
      <h1>It's birding time!</h1>
    );
  }

  return (null);
}
