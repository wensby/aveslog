import React from 'react';

export default function SightingDetails(props) {
  return `I am a SightingDetails${props.match.params.sightingId}`;
}
