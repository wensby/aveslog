import { useState, useEffect, useContext } from "react";
import { AuthenticationContext } from "../authentication/AuthenticationContext";
import axios from 'axios';

export function usePermissions() {
  const [permissions, setPermissions] = useState([]);
  const { authenticated } = useContext(AuthenticationContext);

  useEffect(() => {
    const resolvePermissions = async () => {
      const response = await axios.get('/api/account/roles');
      if (response.status === 200) {
        const json = response.data;
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
