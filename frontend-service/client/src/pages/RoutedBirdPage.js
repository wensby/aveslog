import React, { useState, useEffect } from 'react';
import { BirdPage } from 'bird/BirdPage.js';
import { Redirect } from 'react-router';
import { useTitle } from 'specific/TitleContext';

export default ({ match }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/bird-pages/${match.params.birdId}`)
      .then(response => response.json())
      .then(json => {
        setLoading(false);
        setData(json);
      })
      .catch(error => setError(error));
  }, [match]);

  // useTitle(commonName);
  if (data) return <BirdPage data={data} />;
  else if (error) return <Redirect to='/home' />;
  else return null;
};
