import React, { useState, useEffect } from 'react';

const ScrollContext = React.createContext();

function ScrollProvider(props) {
  const [windowScroll, setWindowScroll] = useState(0);

  const recordWindowScroll = () => {
    setWindowScroll(window.scrollY);
  };

  useEffect(() => {
    window.addEventListener('scroll', recordWindowScroll);
    return () => window.removeEventListener('scroll', recordWindowScroll);
  }, []);

  return (
    <ScrollContext.Provider value={{ windowScroll }} >
      {props.children}
    </ScrollContext.Provider>
  );
}

export { ScrollProvider, ScrollContext }
