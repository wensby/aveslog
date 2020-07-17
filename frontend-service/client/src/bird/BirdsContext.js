import React, { useState, useCallback } from 'react';

const BirdsContext = React.createContext();

const BirdsProvider = ({ children }) => {
  const [birds, setBirds] = useState(new Map());

  const addBird = useCallback(bird => {
    setBirds(prevBirds => {
      const newMap = new Map(prevBirds);
      newMap.set(bird.id, bird);
      return newMap;
    });
  }, [setBirds]);

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
