import React, { useState } from 'react';

const BirdsContext = React.createContext();

const BirdsProvider = ({ children }) => {
  const [birds, setBirds] = useState({});

  const addBird = bird => {
    setBirds(prevBirds => {
      return { ...prevBirds, [bird.id]: bird }
    });
  };

  const contextValues = {
    birds,
    addBird
  };

  return (
    <BirdsContext.Provider value={contextValues}>
      {children}
    </BirdsContext.Provider>
  );
}

export { BirdsContext, BirdsProvider };
