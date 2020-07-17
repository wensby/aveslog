import React, { createContext, useState } from 'react';

const HomeContext = createContext();

const HomeProvider = ({ children }) => {
  const [homeTrigger, setHomeTrigger] = useState(0);

  const incrementHomeTrigger = () => {
    setHomeTrigger(homeTrigger+1);
    console.log('increment');
  };

  const value = {
    homeTrigger, 
    incrementHomeTrigger,
  };

  return (
    <HomeContext.Provider value={value} >
      {children}
    </HomeContext.Provider>
  );
};

export { HomeProvider, HomeContext };
