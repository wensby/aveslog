import { useState, useEffect, useContext } from "react";
import { UserContext } from '../authentication/UserContext';
import AccountService from '../account/AccountService';

export function usePermissions() {
  const [permissions, setPermissions] = useState([]);
  const { authenticated, accessToken } = useContext(UserContext);

  useEffect(() => {
    const resolvePermissions = async () => {
      const response = await fetch(`${window._env_.API_URL}/account/roles`, {
        headers: {
          'accessToken': accessToken.jwt
        }
      });
      if (response.status === 200) {
        const json = await response.json();
        setPermissions(json.items.reduce((list, obj) => {
          const permissions = obj.permissions;
          list.push(...permissions);
          return list;
        }, []));
      }
    };
    if (authenticated) {
      resolvePermissions();
    }
  }, [authenticated]);

  return { permissions };
}

export function useResourcePermission(resource, method) {
  const { permissions } = usePermissions();
  const [present, setPresent] = useState(false);

  useEffect(() => {
    setPresent(permissions
      .filter(x => x.method === method)
      .filter(x => RegExp(x.resource_regex).test(resource)).length > 0);
  }, [permissions, resource, method]);

  return present;
}

export const useAccount = username => {
  const { accessToken, authenticated } = useContext(UserContext);
  const [loading, setLoading] = useState(true);
  const [account, setAccount] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAccount = async () => {
      setLoading(true);
      const response = await new AccountService().fetchAccount(accessToken, username);
      if (response.status === 200) {
        setAccount(await response.json());
      }
      else {
        setError((await response.json()).message);
      }
      setLoading(false);
    };
    setAccount(null);
    setError(null);
    fetchAccount();
  }, [username, authenticated])

  return { loading, account, error }
};
