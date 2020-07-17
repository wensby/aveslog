import React, { createContext, useState, useEffect, useContext } from 'react';

const TitleContext = createContext();

const TitleProvider = ({ children }) => {
  const [title, setTitle] = useState(null);

  useEffect(() => {
    if (title) document.title = title;
    else document.title = 'Aveslog';
  }, [title]);

  return (
    <TitleContext.Provider value={{ setTitle }} >
      {children}
    </TitleContext.Provider>
  );
}

const useTitle = (title) => {
  const { setTitle } = useContext(TitleContext);
  useEffect(() => {
    setTitle(title);
    return () => setTitle(null);
  }, [title]);
}

export { TitleProvider, TitleContext, useTitle }
