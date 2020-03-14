import { useState, useEffect, useContext } from "react";
import { AuthenticationContext } from "../authentication/AuthenticationContext";

export function usePermissions() {
  const [permissions, setPermissions] = useState([]);
  const { authenticated, getAccessToken } = useContext(AuthenticationContext);

  useEffect(() => {
    const resolvePermissions = async () => {
      const accessToken = await getAccessToken();
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
    setPermissions([]);
    if (authenticated) {
      resolvePermissions();
    }
  }, [authenticated, getAccessToken]);

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
