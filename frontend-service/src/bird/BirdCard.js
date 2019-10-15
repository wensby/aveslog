import React from 'react';
import { Link } from "react-router-dom";
import BirdCardPicture from './BirdCardPicture';

export default ({bird, key, children}) => {

  const formattedName = bird.binomialName.toLowerCase().replace(' ', '-');

  return (<div key={key} className="card">
    <div className="card-horizontal">
      <div className="img-square-wrapper">
        <Link to={`/bird/${formattedName}`}>
          <BirdCardPicture bird={bird} />
        </Link>
      </div>
      {children}
    </div>
  </div>);
};
