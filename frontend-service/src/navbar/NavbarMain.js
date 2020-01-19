import React, { useContext } from 'react';
import { Link } from "react-router-dom";
import { UserContext } from '../authentication/UserContext.js';

export function NavbarMain() {
  const { authenticated, account } = useContext(UserContext);

  const renderUsername = () => {
    if (authenticated && account) {
      return (<div className='navbar-username'>
        <Link to={`/profile/${account.username}`}>
          {account.username}
        </Link>
      </div>);
    }
  };

  return (<div className='navbar-main'>
    <Brand />
    {renderUsername()}
  </div>);
}

function Brand() {
  return (
    <div className='brand'>
      <Link to="/" className='text-decoration-none brand-name'>
        Aves<span />log
      </Link>
    </div>
  );
}
