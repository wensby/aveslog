import { useState, useEffect, useContext } from "react";
import { AuthenticationContext } from "../authentication/AuthenticationContext";
import axios from 'axios';

export const usePermissions = () => {
  const [permissions, setPermissions] = useState([]);
  const { authenticated } = useContext(AuthenticationContext);

  useEffect(() => {
    setPermissions([]);
    if (authenticated) {
      axios.get('/api/account/roles')
        .then(response => response.data.items)
        .then(roles => roles.reduce((list, role) => {
          list.push(...role.permissions);
          return list;
        }, []))
        .then(permissions => setPermissions(permissions));
    }
  }, [authenticated]);

  return { permissions };
}

export const useResourcePermission = (resource, method) => {
  const { permissions } = usePermissions();
  const [present, setPresent] = useState(false);

  useEffect(() => {
    const matchingPermissions = permissions
      .filter(permission => permission.method === method)
      .filter(permission => RegExp(permission.resource_regex).test(resource));
    setPresent(matchingPermissions.length > 0);
  }, [permissions, resource, method]);

  return present;
}
