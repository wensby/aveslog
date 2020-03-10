import React from 'react';
import { Link } from 'react-router-dom';

export default function AccountLink({ name }) {
  return (<div>
    <Link to={`/birders/${name}`}>{name}</Link>
  </div>);
}
