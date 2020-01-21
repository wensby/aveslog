import { useContext } from 'react';
import { UserContext } from './UserContext.js';

export function useAuthentication() {
  const { authenticated, account } = useContext(UserContext);
  if (authenticated) {
    return { account };
  }
  return { };
}
