import React from 'react';

export default function BirdDetails(props) {
  return props.match.params.binomialName;
}
