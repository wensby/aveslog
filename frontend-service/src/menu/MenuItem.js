import React from 'react';
import { Link } from 'react-router-dom';

export const MenuItem = ({ item }) => {
  if (item.link) {
    return <Link to={item.link} onClick={item.action}>{item.label}</Link>;
  }
  else {
    return <div onClick={item.action}>{item.label}</div>
  }
};
