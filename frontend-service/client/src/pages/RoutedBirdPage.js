import React, { useState, useEffect } from 'react';
import { BirdPage } from 'bird/BirdPage.js';
import { Redirect } from 'react-router';
import axios from 'axios';

export default ({ match }) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`/api/bird-pages/${match.params.birdId}`)
      .then(response => response.data)
      .then(json => {
        setData(json);
      })
      .catch(error => setError(error));
  }, [match]);

  // useTitle(commonName);
  if (data) return <BirdPage data={data} />;
  else if (error) return <Redirect to='/home' />;
  else return null;
};
