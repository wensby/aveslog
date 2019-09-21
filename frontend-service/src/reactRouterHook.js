import { useContext } from 'react';
import { __RouterContext } from 'react-router';

export const useReactRouter = () => {
  const routerContext = useContext(__RouterContext);
  return routerContext;
};
