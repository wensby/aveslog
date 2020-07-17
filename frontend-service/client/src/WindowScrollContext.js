import React, { useState, useEffect } from 'react';

const WindowScrollContext = React.createContext();

const WindowScrollProvider = ({ children }) => {
  const [scroll, setScroll] = useState(0);

  const recordScroll = () => {
    setScroll(window.scrollY);
  };

  useEffect(() => {
    window.addEventListener('scroll', recordScroll);
    return () => window.removeEventListener('scroll', recordScroll);
  }, []);

  return (
    <WindowScrollContext.Provider value={{ windowScroll: scroll }} >
      {children}
    </WindowScrollContext.Provider>
  );
}

export { WindowScrollProvider, WindowScrollContext }
