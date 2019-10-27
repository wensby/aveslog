import React, { useContext, useState, useEffect } from 'react';
import SightingFeed from './SightingFeed';
import { UserContext } from '../authentication/UserContext';

export default function SightingFeedContainer({ }) {
  const { getAccessToken } = useContext(UserContext);
  const [sightings, setSightings] = useState([]);
  useEffect(() => {

  }, []);
  return <SightingFeed />;
}
